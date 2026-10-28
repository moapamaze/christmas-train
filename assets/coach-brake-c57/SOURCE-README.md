# C5.7 source and issue

Canonical geometry is checkpoint.brep with ordered parts.json and geometry-contract.json, in millimetres. The C56 brake load path is retained. Of 199 parent parts, 156 are unchanged, 40 local air parts are relocated and 3 air parts are revised; 80 new SUPPLY-* parts form the body-to-truck connection. patch-audit.json records the complete disjoint part lists. The local support moves 50 mm along +X with an extended base and regenerated free hose curves. Independent motion-review.json checks those changed curves against all current hardware and verifies the protected mounting-section parts remain byte-identical. Purchased exterior envelopes and threaded engagements retain their stated limits.

Build order: build_c57.py; check_motion_c57.py; check_service_c57.py; issue_c57.py; issue_motion_c57.py; draw_air_c57.py; draw_service_c57.py; finalize_c57.py. The independent checks read frozen BREP and contracts, not the geometry builder. Any changed geometry requires all dependent checks and drawings to be reissued.

Site: scripts/coach-current/build_c57_page.py then integrate_c57.py; verify_c57_site.py and verify_c57_truck.mjs validate the issued links/model composition. Compact_c57_transport.py is lossless legacy transport packaging, not geometry deletion. The shared wheelset/assembled-coach and locomotive workstreams remain separate.

These are development artifacts. Missing supplier data, unresolved hose end-clock compatibility, production hose instructions, exact tool/pad access and structural/fatigue acceptance remain explicit. No brake unit is repeated or fabrication/operation released.
