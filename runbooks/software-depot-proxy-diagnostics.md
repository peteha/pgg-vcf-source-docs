# Troubleshoot VCF Software Depot proxy connections

**Status:** Draft. Broadcom documents the depot pod and `download-service` logs for VCF 9.1. The commands below have not yet been validated against a 9.1.1 runtime.

This read-only investigation helps identify a failed Software Depot request and correlate it with a customer proxy's access logs. It covers a **connected Software Depot** on VCF 9.1.x. A bastion or VCF Download Tool has its own proxy configuration and requires separate logs.

A failed download alone does not prove an allowlist problem. A matching denial in the proxy log is the evidence needed to identify the rule and destination.

## Before you begin

- Use an authorized, read-only shell and Kubernetes context for the **VCF services runtime hosting the affected depot**. Do not use a Supervisor or workload-cluster context by mistake.
- Confirm the deployed version, runtime access procedure, namespace, pod and container names. The documented 9.1 names below still need verification against the exact customer build.
- Logs can contain credentials, tokens, signed URLs and customer information. Inspect them locally under the customer's controls and sanitize before sharing. Do not print environment variables, proxy credentials, configuration secrets or raw API responses.
- If SSH is disabled, enabling it is a separate configuration change. Do not trigger a download solely to capture logs unless the customer authorizes a bounded test.

## 1. Establish the failure

In VCF Operations, identify the affected Software Depot and its connection mode. Record the VCF version, affected runtime instance, failing action, approximate time and time zone. Start with **Operate → Logs** if log management is available.

For direct runtime access, identify the affected services runtime control-plane node under **Build → Lifecycle → VCF Management → Components → VCF services runtime → Nodes**. Use the customer's authorized administrator and the release-specific documented SSH procedure.

Ask the proxy team for the proxy endpoint and the runtime's actual egress source IP or addresses as observed by the proxy. A runtime can have multiple source IPs.

## 2. Identify the depot workload

In the approved runtime context, run:

```sh
kubectl config current-context
kubectl get namespaces
kubectl -n vcf-fleet-depot get pods -o wide
```

Confirm the context and namespace with the administrator. If the namespace does not exist, stop and obtain the supported route for that release. Select the depot pod from the output and list its container names:

```sh
kubectl -n vcf-fleet-depot get pod <depot-pod> \
  -o jsonpath='{.spec.containers[*].name}{"\n"}'
```

[Broadcom KB 453506](https://knowledge.broadcom.com/external/article/453506/validation-of-offline-software-depot-fai.html) identifies the pod as `depot-service-<suffix>` and the application container as `download-service` for VCF 9.1. Confirm both appear in the deployment; do not substitute the file-server, gateway or registry container.

## 3. Inspect the failure window

Replace `<depot-pod>` with the verified pod name. Choose a short window around the failure; 30 minutes is an example:

```sh
kubectl -n vcf-fleet-depot logs <depot-pod> \
  -c download-service --since=30m --timestamps | less
```

Review the output in the customer's secure terminal. In `less`, search for `/proxy`, `/403`, `/407`, `/timeout`, `/certificate`, or the destination hostname. Press `n` for the next match and `q` to exit. If the container restarted, repeat with `--previous`; previous logs may not be available.

Record only the timestamp, destination hostname and port, sanitized error class, and request ID if present. A line mentioning an HTTP status does not by itself establish which intermediary returned it.

For support bundles, [KB 453215](https://knowledge.broadcom.com/external/article/453215/proxy-configuration-for-vcf-management-s.html) identifies `vcf-fleet-depot/<node_name>/depot-service-<identifier>/download-service/console-log`. This is a **bundle location**, not a verified path on the live filesystem.

## 4. Correlate with the proxy

Give the proxy team the failure window and time zone, observed runtime source IP, destination host and port, and request ID if available. Ask for the proxy's policy decision, authentication outcome and any redirect or additional destination. Match the timestamp and source IP with the depot event.

| Observation | What to check next |
| --- | --- |
| Proxy log shows a deny or policy rule | Identify the exact destination, port, source and rule; ask the proxy owner to evaluate the allowlist. |
| `407 Proxy Authentication Required` | Check proxy authentication configuration and the proxy log. Do not expose or rotate credentials as part of diagnosis. |
| `403 Forbidden` | Identify whether the proxy or upstream returned it and inspect the matching proxy decision; 403 alone does not prove an allowlist block. |
| Certificate or trust failure | Check the certificate chain and whether TLS interception requires the proxy CA in the depot truststore. Use the release-specific Broadcom procedure. |
| Timeout or no matching proxy record | Check the source IP, time window, DNS, routing, firewall and whether the runtime uses the proxy. Absence from a log is not proof of direct egress. |
| Upstream `401` or `404` | Investigate upstream entitlement, credentials or artifact availability; do not assume the proxy is responsible. |

## 5. Compare with the vendor destination list

The VCF 9.1.x guide lists the following for binary downloads:

- `dl.broadcom.com`
- `eapi.broadcom.com`
- `vvs.broadcom.com`
- `vsanhealth.vmware.com`
- `vcf.packages.broadcom.com` for 9.1.1 and later

Supervisor and VCF service downloads also list `projects.packages.broadcom.com`. The documented destination port is **443**.

Use the current vendor list for the exact release and enabled features. This is not a complete firewall allowlist; CDN redirects and the proxy's policy model may require further investigation. PAIS mirroring and bastion tools have separate source and proxy paths.

## 6. Confirm the fix

Once the customer approves any proxy change, repeat one agreed, bounded operation and correlate the depot result with an allow decision in the proxy logs. Record the destination, source, timestamp, rule and outcome. Do not disable TLS validation or bypass the proxy to make the test pass.

## Sources and limits

- [VMware Cloud Foundation 9.1.x](https://techdocs.broadcom.com/content/dam/broadcom/techdocs/us/en/pdf/vmware/vcf/vcf-90/vmware-cloud-foundation-9-1.pdf): public URLs pp. 2442–2443; Software Depot pp. 3976–3979; proxy configuration pp. 4498–4503.
- [Broadcom KB 453506](https://knowledge.broadcom.com/external/article/453506/validation-of-offline-software-depot-fai.html): VCF 9.1 depot pod and `download-service` logs.
- [Broadcom KB 453215](https://knowledge.broadcom.com/external/article/453215/proxy-configuration-for-vcf-management-s.html): support-bundle log location.
- [Broadcom KB 442978](https://knowledge.broadcom.com/external/article/442978): services-runtime proxy configuration and trust.

No lab or customer example is claimed here. The exact runtime access route and commands are awaiting 9.1.1 lab validation.
