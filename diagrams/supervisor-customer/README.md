# Connected software depot: Supervisor and VKS content paths

Customer-facing draft, VCF 9.1.x, including management and lifecycle binaries as well as Supervisor and VKS content. Outbound arrows show requests initiated by the software depot through the customer proxy; the lower arrows show content distribution. Proxy configuration is per VCF services runtime instance, not necessarily a single fleet-wide setting. The destination list is representative, not a complete firewall allowlist. VCF 9.1.1 adds vcf.packages.broadcom.com to the documented download destinations.

Source: VMware Cloud Foundation 9.1.x, 2026-10-13 edition: Public URLs Required for Online Functionalities, pp. 2442–2443; Configure a Proxy Server for VCF Management Services Components, pp. 4498–4503; Supervisor artifacts and Software Depot pp. 6866–6868; Supervisor content libraries pp. 7008–7017. VCF Service Administration and Development 9.1: regional Harbor pp. 249–252. The management arrows represent content availability, not an established instance-level staging sequence. These are documentary paths, not customer-specific validation. See the PGG-696 validation register for wider assumptions.

Run `python3 generate.py` in this directory to regenerate the editable SVG and PNG. Style primitives are adapted from jazzy/pgg-696 `docs/diagrams/vcf-source/src/bcstyle.py`.
