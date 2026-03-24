"""
Short Article workflow implementation.

This workflow implements the 5-step translation process for articles
and similar content types.
"""

from typing import List, Dict, Any
from ...core.context import TranslationContext
from ...core.workflow import AbstractWorkflow
from .aux.parsers import parse_analysis, parse_translation

class ShortArticleWorkflow(AbstractWorkflow):
    """
    Workflow for translating articles and similar content.

    This workflow implements the proven 5-step process using direct methods:
    1. analyze() - Identify key terms and concepts
    2. search() - Generate contextual explanations with web search
    3. translate() - Create initial translation
    4. critique() - Evaluate translation quality
    5. refine() - Produce final improved translation

    To customize: simply inherit from this class and override any method.
    """

    def get_workflow_name(self) -> str:
        """Get the unique name of this workflow."""
        return "short_article"

    def is_suitable_for(self, text: str, **_kwargs) -> bool:
        """
        Determine if this workflow is suitable for the given content.

        This workflow is suitable for:
        - Articles and blog posts
        - General text content
        - Serves as the default workflow when no other workflow matches

        Args:
            text: The text content to evaluate
            **kwargs: Additional evaluation parameters

        Returns:
            bool: True if this workflow is suitable
        """
        # This workflow accepts any non-empty text
        return len(text.strip()) > 0

    def analyze(self, context: TranslationContext, text: str) -> List[Dict[str, Any]]:
        """
        Analyze the source text to identify key terms and concepts.

        Args:
            context: The translation context
            text: The text to analyze

        Returns:
            List[Dict]: Parsed analysis results with term names and keywords
        """
        # Get writer model from workflow configuration
        writer_model = context.get_workflow_config('writer')

        # Get prompts for analysis
        system_prompt = self.get_prompt(
            'step1_system.txt',
            post_content=text,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step1_user.txt',
            post_content=text,
            source_language=context.source_language,
            target_language=context.target_language
        )

        # Call LLM for analysis
        analysis_content = context.model_client.call_model(
            system_prompt,
            user_prompt,
            writer_model,
            log_call=context.log_calls
        )

        # Parse and return analysis
        return parse_analysis(analysis_content)

    def search(self, context: TranslationContext, parsed_items: List[Dict[str, Any]]) -> str:
        """
        Generate contextual explanations for analyzed terms using web search.

        Args:
            context: The translation context
            parsed_items: List of terms from analysis step

        Returns:
            str: Formatted glossary content
        """
        if not parsed_items:
            return ""

        # Get searcher model from workflow configuration
        searcher_model = context.get_workflow_config('searcher')
        glossary = []

        for item in parsed_items:
            # Generate explanation for each term using web search
            term_explanation = self._generate_term_explanation(context, item, searcher_model)

            # Format glossary entry
            glossary_entry = (
                f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n"
                f"**Explanation:**\n{term_explanation}\n"
            )
            glossary.append(glossary_entry)

        return "\n".join(glossary)

    def translate(self, context: TranslationContext, text: str) -> str:
        """
        Create the initial translation of the source text.

        Args:
            context: The translation context
            text: The text to translate

        Returns:
            str: The initial translation
        """
        # Get writer model from workflow configuration
        writer_model = context.get_workflow_config('writer')

        # Get prompts for translation
        system_prompt = self.get_prompt(
            'step3_system.txt',
            text=text,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step3_user.txt',
            text=text,
            source_language=context.source_language,
            target_language=context.target_language
        )

        # Call LLM for translation
        return context.model_client.call_model(
            system_prompt,
            user_prompt,
            writer_model,
            log_call=context.log_calls
        )

    def critique(self, context: TranslationContext, text: str,
                 translation: str, glossary: str) -> str:
        """
        Evaluate the translation quality and provide feedback.

        Args:
            context: The translation context
            text: The original text
            translation: The initial translation
            glossary: The glossary from search step

        Returns:
            str: Critique and feedback
        """
        # Get critiquer model from workflow configuration
        critiquer_model = context.get_workflow_config('critiquer')

        # Get prompts for critique
        system_prompt = self.get_prompt(
            'step4_system.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step4_user.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            source_language=context.source_language,
            target_language=context.target_language
        )

        # Call LLM for critique
        return context.model_client.call_model(
            system_prompt,
            user_prompt,
            critiquer_model,
            log_call=context.log_calls
        )

    def refine(self, context: TranslationContext, text: str, *,
               translation: str, glossary: str, critique: str) -> str:
        """
        Produce the final refined translation based on critique feedback.

        Args:
            context: The translation context
            text: The original text
            translation: The initial translation
            glossary: The glossary from search step
            critique: The critique feedback

        Returns:
            str: The final refined translation
        """
        # Get writer model from workflow configuration
        writer_model = context.get_workflow_config('writer')

        # Get prompts for refinement
        system_prompt = self.get_prompt(
            'step5_system.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            critique=critique,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step5_user.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            critique=critique,
            source_language=context.source_language,
            target_language=context.target_language
        )

        # Call LLM for refinement
        final_translation_content = context.model_client.call_model(
            system_prompt,
            user_prompt,
            writer_model,
            log_call=context.log_calls
        )

        # Parse and return final translation
        return parse_translation(final_translation_content)

    def execute(self, context: TranslationContext, text: str) -> str:
        """
        Execute the complete short article workflow.

        This method orchestrates the 5-step process in sequence.

        Args:
            context: The translation context
            text: The text to translate

        Returns:
            str: The final refined translation
        """
        # Step 1: Analyze the text to identify key terms
        analysis = self.analyze(context, text)

        # Step 2: Search for contextual information about the terms
        glossary = self.search(context, analysis)

        # Step 3: Create initial translation
        translation = self.translate(context, text)

        # Step 4: Critique the translation
        critique = self.critique(context, text, translation, glossary)

        # Step 5: Refine the translation based on critique
        final_translation = self.refine(context, text, translation=translation,
                                        glossary=glossary, critique=critique)

        return final_translation

    def _generate_term_explanation(self, context: TranslationContext,
                                   item: Dict[str, Any], model: str) -> str:
        """
        Generate explanation for a single term using web search.

        Args:
            context: The translation context
            item: Dictionary with 'name' and 'keywords' keys
            model: The model to use for generation

        Returns:
            str: The generated explanation with web search results
        """
        system_prompt = self.get_prompt(
            'step2_system.txt',
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step2_user.txt',
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=context.source_language,
            target_language=context.target_language
        )

        return context.model_client.call_model(
            system_prompt,
            user_prompt,
            model,
            log_call=context.log_calls,
            enable_web_search=True,
            web_search_context="high"
        )
