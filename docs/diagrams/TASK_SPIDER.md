%% Task Spider — Orchestration Organism
%% Decomposes tasks, dispatches agents, senses tension, recombines outputs.

flowchart TD

    subgraph SPIDER["Task Spider (Orchestration Organism)"]
        DECOMP["Task Decomposition\n• Identity limb\n• Routing limb\n• Logistics limb\n• Audit limb\n• Safety limb\n• Translation limb"]
        AGENTS["Agent Limbs\n• Parallel execution"]
        TENSION["Tension Sensing\n• Errors\n• Anomalies\n• Unsafe routes\n• Treaty violations"]
        MERGE["Recombination\n• Collect outputs\n• Validate\n• Governed result"]
    end

    %% Flow inside Task Spider
    DECOMP --> AGENTS --> TENSION --> MERGE

    %% Output to User World
    MERGE --> WORLD["User World"]
