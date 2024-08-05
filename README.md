# 🌐💬 Aphra

```mermaid
flowchart LR
    T[📄 Original Text]
    
    subgraph "1. Analysis"
        direction TB
        A[fa:fa-robot LLM Writer] -->C[fa:fa-file-alt Glossary]
    end
    
    subgraph "2. Search"
        direction TB
        D[fa:fa-search LLM Searcher] --> F[fa:fa-file-alt Contextualized Glossary]
    end
    
    subgraph "3. Initial Translation"
        direction TB
        G[fa:fa-robot LLM Writer] -->H[fa:fa-language Basic Translation]
    end
    
    subgraph "4. Critique"
        direction TB
        I[fa:fa-balance-scale LLM Critic] --> J[fa:fa-comments Critique]
    end
    
    subgraph "5. Final Translation"
        direction TB
        K[fa:fa-robot LLM Writer] --> L[fa:fa-check-circle Final Translation]
    end

    T --> A
    T --> G
    C --> D
    F --> I
    H --> I
    T --> K
    H --> K
    F --> K
    J --> K
    
    classDef default fill:#abb,stroke:#333,stroke-width:2px;
    classDef robot fill:#bbf,stroke:#333,stroke-width:2px;
    classDef document fill:#bfb,stroke:#333,stroke-width:2px;
    classDef search fill:#fbf,stroke:#333,stroke-width:2px;
    classDef critic fill:#ffb,stroke:#333,stroke-width:2px;
    class A,G,K robot;
    class T,B,C,F,H,L document;
    class D search;
    class I,J critic;
```
