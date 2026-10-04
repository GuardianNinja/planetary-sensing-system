%% Governance Layer — Constitutional Backbone
%% Governs identity, evidence, access lanes, safety, and treaties.

flowchart TD

    subgraph GOV["Governance Layer"]
        IDENTITY["Identity Spine\n• QR‑DNA\n• Lineage keys"]
        EVIDENCE["Evidence Ledger\n• Immutable records\n• Cross‑domain truth"]
        ACCESS["Access Law\n• CIV / CORP / MIL lanes"]
        SAFETY["Safety Kernel\n• Non‑overrideable logic"]
        TREATIES["Domain Treaties\n• World‑to‑world contracts"]
    end

    %% Sequential governance flow
    IDENTITY --> EVIDENCE --> ACCESS --> SAFETY --> TREATIES

    %% Output to HI Kernel
    TREATIES --> HIKERNEL["HI Kernel"]
