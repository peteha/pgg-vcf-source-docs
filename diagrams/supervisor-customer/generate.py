#!/usr/bin/env python3
"""Generate the connected VCF depot content paths."""
from pathlib import Path
import subprocess
import bcstyle as b
out=Path(__file__).resolve().parent
k=b.K
s=b.header('VCF 9.1.x  ·  Connected Software Depot', 'Broadcom software paths across the VCF fleet',
           'The Software Depot requests external content through the customer proxy and makes it available to VCF consumers.')
s+=b.t(40,150,'Grey arrows: outbound requests     ·     Teal: software and OVF content     ·     Purple: OCI artifacts     ·     Dashed: optional path',17,k['slate'])
# Five main boxes
s+=b.panel(40,200,440,1050,'Broadcom online sources','Representative HTTPS destinations · port 443',k['slate'],k['design'],'source')
s+=b.panel(550,200,320,1050,'Customer proxy','Outbound network access',k['navy'],k['cyan'],'proxy')
s+=b.panel(940,200,700,1050,'VCF Services','Software Depot / Lifecycle · fleet-level',k['purple'],k['navy'],'runtime')
s+=b.panel(1700,200,460,1050,'Distribution','Content paths',k['navy'],k['cyan'],'distribution')
s+=b.panel(2230,200,530,1050,'VCF fleet and region','Management and workload consumers',k['purple'],k['navy'],'region')
# External destinations
for y,title,sub in [(290,'dl.broadcom.com','VCF binaries'),(410,'eapi.broadcom.com','Authorization and services'),(530,'vvs.broadcom.com','Documented VCF download host'),(650,'vsanhealth.vmware.com','Documented VCF download host'),(770,'projects.packages.broadcom.com','Supervisor and VCF service artifacts'),(890,'vcf.packages.broadcom.com','VCF 9.1.1 and later')]:
 s+=b.card(60,y,400,94,'cloud',title,(sub,))
s+=b.card(570,580,280,130,'proxy','Proxy service',('Customer endpoint', 'Site trust and authentication'))
# VCF Services: lifecycle and Software Depot components
s+=b.card(985,310,610,110,'ops','Binary Management',('VCF Operations manages lifecycle software',))
s+=b.card(985,500,610,260,'box','Software Depot',('Binaries, OVFs and OCI artifacts', 'OCI registry interface serves registry content', 'Proxy configured per VCF services runtime'))
# Distribution
s+=b.card(1720,685,420,135,'library','vCenter content library',('Subscribed to the depot', 'Supervisor and VKr OVFs'))
s+=b.card(1720,995,420,130,'registry','Regional Harbor',('Project vcf proxies the', 'depot OCI registry'),border=k['purple'],ic=k['purple'])
s+=b.card(1720,1145,420,80,'registry','Optional Harbor',('Alternative registry path;', 'site-specific content and trust'),border=k['purple'],ic=k['purple'])
# Consumers
s+=b.card(2250,310,490,110,'cluster','SDDC Manager and VCF lifecycle',('Management installation, upgrade and patch', 'binaries for VCF instances'))
s+=b.card(2250,700,490,110,'k8s','Supervisor',('Control plane image: OVF',),ic=k['purple'])
s+=b.card(2250,850,490,110,'k8s','VKS clusters',('VKr OVF and OCI add-ons',),ic=k['purple'])
s+=b.card(2250,1010,490,100,'app','Supervisor Services',('OCI packages and images',),border=k['purple'],ic=k['purple'])
s+=b.card(2250,1135,490,90,'plugin','VCF CLI plug-ins',('OCI packages',),border=k['purple'],ic=k['purple'])
# Outbound connection initiated by depot; hub fans out to each destination
s+=b.arrow([(985,655),(900,655),(900,645),(850,645)],k['slate'],sw=2.6)
s+=b.arrow([(570,645),(520,645)],k['slate'],sw=2.6,head=False)
s+=f'<path d="M 520 337 L 520 937" stroke="{k["slate"]}" stroke-width="2.6" fill="none"/>'
for y in (337,457,577,697,817,937): s+=b.arrow([(520,y),(460,y)],k['slate'],sw=2.6)
s+=b.t(895,600,'outbound request',14,k['slate'],700,'end')
# Content flows
s+=b.arrow([(1010,500),(970,500),(970,365),(985,365)],k['teal'],sw=3)
s+=b.arrow([(1595,752),(1720,752)],k['teal'],sw=3)
s+=b.arrow([(1595,365),(2250,365)],k['teal'],sw=3)
s+=b.arrow([(2140,752),(2250,752)],k['teal'],sw=3)
s+=b.arrow([(2140,790),(2190,790),(2190,905),(2250,905)],k['teal'],sw=3)
s+=b.arrow([(1595,700),(1655,700),(1655,1060),(1720,1060)],k['purple'],sw=3)
s+=b.arrow([(2140,1020),(2210,1020),(2210,905),(2250,905)],k['purple'],sw=3)
s+=b.arrow([(2140,1060),(2250,1060)],k['purple'],sw=3)
s+=b.arrow([(2140,1095),(2190,1095),(2190,1180),(2250,1180)],k['purple'],sw=3)
# Optional alternate registry is intentionally not asserted as a depot proxy
s+=f'<path d="M2140 1185 H2220 Q2230 1185 2230 1175 V1080 Q2230 1070 2240 1070 H2250" fill="none" stroke="{k["purple"]}" stroke-width="3" stroke-dasharray="8 6"/>'
s+=f'<path d="M2250 1070 l-12 -6 v12 z" fill="{k["purple"]}"/>'
s+=f'<circle cx="2115" cy="1145" r="16" fill="white" stroke="{k["purple"]}" stroke-width="2"/>'
s+=b.t(2115,1151,'1',16,k['purple'],700,'middle')
# Manual acquisition and mirroring is a separate host and has its own proxy configuration.
s+=b.panel(940,1300,1150,245,'Manual process (bastion / admin host)', 'Separate host; configure its own network access and proxy', k['navy'],k['cyan'],'manual')
s+=b.card(965,1390,500,110,'download','VMDT / VCF Download Tool',('Downloads VCF depot content', 'and uploads artifacts when required'))
s+=b.card(1535,1390,530,110,'upload','VCF commands: PAIS AMT',('Pulls PAIS and third-party artifacts', 'and pushes them to a Harbor project'),border=k['purple'],ic=k['purple'])
s+=b.arrow([(965,1445),(920,1445),(920,760),(985,760)],k['teal'],sw=3)
s+=b.arrow([(1800,1390),(1800,1225)],k['purple'],sw=3)
s+=b.arrow([(940,1515),(895,1515),(895,735),(710,735),(710,710)],k['slate'],sw=2.6)
s+=b.t(720,765,'bastion outbound',14,k['slate'],700)
s+=b.t(40,1585,'1  PAIS mirrored to an optional Harbor requires the external PAIS YAML definition; AMT generates the installation and service configuration YAML files.',16,k['ink'],700)
s+=b.t(40,1615,'Connected mode above; manual flows are separate workflows. VCF Download Tool uploads and PAIS AMT mirroring have distinct purposes.',16,k['slate'])
s+=b.t(40,1645,'Optional Harbor content, supported use and trust depend on the workflow. Management arrows do not prove an instance-level staging sequence.',16,k['slate'])
s+=b.t(40,1675,'Sources: VCF 9.1.x pp. 2442–2443, 3973–3979, 4498–4503; Private AI Foundation 9.1 pp. 99–113.',16,k['slate'])
svg=out/'supervisor-content-paths.svg'
svg.write_text(b.svg(2800,1700,s),encoding='utf-8')
subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--hide-scrollbars','--window-size=2800,1700','--force-device-scale-factor=2',f'--screenshot={out / "supervisor-content-paths.png"}',svg.as_uri()],check=True,capture_output=True,timeout=90)
