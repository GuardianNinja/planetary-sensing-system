%% User World — Sovereign Digital Territory
%% Local OS, identity, evidence, shield, ports, local spider.

flowchart TD

    subgraph WORLD["User World (Sovereign Node)"]
        OS["Local OS Layer\n• Shadow‑X style"]
        IDDOM["Identity Domain\n• Personal lineage"]
        EVCACHE["Local Evidence Cache\n• Private truth store"]
        SHIELD["Shielded Perimeter\n• Planetary Skin node"]
        PORTS["Integration Ports\n• Treaty‑bound\n• Audited"]
        LOCALSPIDER["Local Task Spider\n• Local agents"]
    end

    %% Internal world flow
    OS --> IDDOM --> EVCACHE --> SHIELD --> PORTS --> LOCALSPIDER

    %% Output to Planetary Skin
    SHIELD --> SKIN["Planetary Skin Mesh"]
