# fritz-rebooter
Simple service to trigger a Internet re-connect for a Fritz!Box

Idea is to have an automated [internet-speed-monitoring](https://github.com/sthuber90/docker-speedtest) in place and use [Grafana-Alerts](https://grafana.com/docs/grafana/latest/alerting/) to define and check a "Internet is down" condition. If the condition is met, this can trigger a Webhook to the here defined REST endopint that in turn triggers a re-connect of the Internet connection which sould resole the connectivity issues.

Cheers,
Jan
