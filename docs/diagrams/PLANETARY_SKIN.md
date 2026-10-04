%% Planetary Skin — Global Mesh Ecosystem
%% Distributed shield, routing, tension sensing, environmental memory.

flowchart TD

    subgraph SKIN["Planetary Skin Mesh"]
        NODES["Mesh Nodes\n• All user worlds"]
        TENSION["Tension Sensing\n• Events\n• Anomalies\n• Signals"]
        SHIELDLOGIC["Distributed Shield Logic\n• Throttling\n• Quarantine\n• Isolation"]
        ROUTING["Domain Routing\n• Safe world‑to‑world travel"]
        INTEGRITY["Collective Integrity\n• More nodes = stronger mesh"]
        MEMORY["Environmental Memory\n• Ecosystem‑level patterns"]
    end

    %% Mesh flow
    NODES --> TENSION --> SHIELDLOGIC --> ROUTING --> INTEGRITY --> MEMORY

    %% Output back to User Worlds
    ROUTING --> WORLD["User Worlds"]
