%% HI Kernel — Brainstem of the Digital Organism
%% Converts human intent into structured tasks and activates Task Spider.

flowchart TD

    subgraph HI["HI Kernel (Brainstem)"]
        INTENT["Intent Interpreter\n• Human → structured task\n• No hallucination"]
        GOVCHECK["Governance Checkpoint\n• Identity\n• Evidence\n• Access\n• Safety"]
        SPIDER_ACT["Task Spider Activation\n• Decomposition trigger"]
        RECOMBINE["Recombination Layer\n• Merge agent outputs\n• Validate via ledger"]
    end

    %% Flow inside HI Kernel
    INTENT --> GOVCHECK --> SPIDER_ACT --> RECOMBINE

    %% Output to Task Spider
    RECOMBINE --> SPIDER["Task Spider"]
