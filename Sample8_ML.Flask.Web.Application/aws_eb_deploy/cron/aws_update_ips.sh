#!/bin/bash


# Log start time
echo "Starting AWS IP update script at $(date)" >> /dev/stdout 2>> /dev/stderr

# Use the URL from the environment variable if provided, otherwise use the default
AWS_IP_RANGES_URL=${AWS_IP_RANGES_URL:-$DEFAULT_AWS_IP_RANGES_URL}

# Fetch AWS IP ranges with TLS 1.2
curl -s --tlsv1.2 "$AWS_IP_RANGES_URL" -o /etc/nginx/modsecurity/aws_ips/ip-ranges.json

# Extract IP ranges for relevant AWS services and save to a text file
jq -r '.prefixes[] |
       select(
          .service == "EC2" or .service == "S3" or .service == "ECS" or
          .service == "CLOUDFRONT" or .service == "AMAZON" or .service == "ROUTE53" or
          .service == "CHIME_VOICECONNECTOR" or .service == "ROUTE53_HEALTHCHECKS" or
          .service == "GLOBALACCELERATOR" or .service == "EBS" or .service == "ROUTE53_RESOLVER" or
          .service == "API_GATEWAY" or .service == "CODEBUILD" or .service == "CLOUD9" or
          .service == "CLOUDFRONT_ORIGIN_FACING" or .service == "CHIME_MEETINGS" or
          .service == "ROUTE53_HEALTHCHECKS_PUBLISHING" or .service == "AMAZON_CONNECT" or
          .service == "DYNAMODB" or .service == "MEDIA_PACKAGE_V2" or
          .service == "AMAZON_APPFLOW" or .service == "WORKSPACES_GATEWAYS" or
          .service == "KINESIS_VIDEO_STREAMS" or .service == "EC2_INSTANCE_CONNECT" or
          .service == "IVS_REALTIME"
       ) | .ip_prefix' /etc/nginx/modsecurity/aws_ips/ip-ranges.json > /etc/nginx/modsecurity/aws_ips/aws_ips.txt

# Generate ModSecurity rules based on the extracted IP ranges
echo "# AWS IP Ranges" > /etc/nginx/modsecurity/aws_ips/aws_ip_whitelist.conf
id=1000000
while read -r ip; do
  echo "SecRule REMOTE_ADDR \"@ipMatch $ip\" \"id:$id,phase:1,pass,nolog,ctl:ruleRemoveById=920350\"" >> \
       /etc/nginx/modsecurity/aws_ips/aws_ip_whitelist.conf
  id=$((id+1))
done < /etc/nginx/modsecurity/aws_ips/aws_ips.txt

# Ensure correct permissions
chmod 644 /etc/nginx/modsecurity/aws_ips/aws_ip_whitelist.conf \
          /etc/nginx/modsecurity/aws_ips/aws_ips.txt \
          /etc/nginx/modsecurity/aws_ips/ip-ranges.json

# Log end time
echo "Finished AWS IP update script at $(date)" >> /dev/stdout 2>> /dev/stderr