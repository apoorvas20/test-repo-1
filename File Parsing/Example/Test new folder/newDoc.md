# Ingest service

The ingest service is a core data processing system that ingests data from external sources (Notion, Linear, GitHub, Zendesk, Google Drive) into Falconer’s knowledge base. 📥

## Architecture🏗️

The service implements a multi-stage pipeline with distinct phases: reception, validation, transformation, and routing. 

### Components⚙️

**Main service** 🎯: Handles API endpoints and orchestrates ingestion jobs

**Workers** 👷: Process ingestion tasks from message queues (BullMQ) ![f>][fl4yvl62xcx05t7czpgtts6w]

**Base connector handler** 🔌: Provides an abstract foundation for implementing data ingestion connectors, managing the lifecycle of connector jobs including initialization, execution, error handling, and status tracking ![f>][ekkiwc3b9ivzit2wwgmlytfr]

## Data flow🌊

### Reception📡

The service accepts data through multiple channels:

- REST API endpoints for synchronous data submission ![f>][ekkiwc3b9ivzit2wwgmlytfr]
- Webhook endpoints for asynchronous notifications from partner systems
- Message queue consumers pulling from Kafka topics for event-driven ingestion
- Batch file uploads via SFTP for legacy integrations

All endpoints implement authentication via API keys or OAuth 2.0 tokens, with rate limiting of 1000 requests/minute per client by default. ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Validation✅

The service enforces multiple validation layers:

- Schema validation using JSON Schema or Avro
- Required field checks and data type validation
- Format validation for emails, phone numbers, URLs
- Range validation for numeric fields
- Referential integrity checks against reference data stores
- Business rule validation for domain-specific logic
- Duplicate detection within a 24-hour window ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Transformation🔄

Data undergoes several transformation steps:

- Field mapping to canonical internal field names
- Data type conversion and date format standardization
- Enrichment with derived fields and reference data lookups
- Normalization of addresses, phone numbers, and currency codes
- PII masking based on data classification policies ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Routing🚦

Messages are routed based on:

- Data type (orders, customers, products)
- Source system or partner
- Priority level (high/medium/low)
- Geographic region for data residency requirements
- Conditional rules evaluating message content ![f>][ekkiwc3b9ivzit2wwgmlytfr]

## Connector lifecycle🔄

The base connector handler manages a standardized job lifecycle:

### Initialization🚀

When `job.data.step` equals ‘init’, the handler:

- Resets all connector status counters to initial values
- Creates an `asyncRun` database record with job metadata
- Sets status counters: STATUS=INGESTING, TOTAL=0, COMPLETED=0, IN_PROGRESS=0, FAILED=0 ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Execution⚡

The handler retrieves enabled source accounts from the database filtered by provider, organization ID, and source status, then processes data according to connector-specific logic. 

### Completion🏁

When `job.data.step` equals ‘post-children’, the handler:

- Updates connector status to COMPLETED
- Updates the `asyncRun` record with completion timestamp
- Populates the summary field with final status counters ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Error handling⚠️

On job failure, the handler:

- Updates the `asyncRun` status to FAILED
- Sets the `completedAt` timestamp
- Populates the summary with status counters ![f>][ekkiwc3b9ivzit2wwgmlytfr]

Validation errors return HTTP 400 responses with detailed error messages. Transient errors trigger automatic retry with exponential backoff (max 5 retries), while permanent errors move messages to dead letter queues without retry. ![f>][ekkiwc3b9ivzit2wwgmlytfr]

## Deployment🚀

### Build process🔨

The service uses Docker for containerization:

```bash
falcon deploy ingest build --env <environment>
```

This builds a Docker image tagged with the git revision and environment, targeting the linux/amd64 platform. ![f>][wv34jbxnv9z53mg7uepewau1]

### Push to ECR📤

After building, images are pushed to Amazon ECR:

```bash
falcon deploy ingest push --env <environment>
```

The push process logs into ECR, tags the image with both the git revision and environment-specific latest tag, then pushes both tags. ![f>][pv4em9kjtd8racrnfr9zqbkz]

### Deployment to ECS☁️

Full deployment orchestrates the build, push, and ECS service update:

```bash
falcon deploy ingest redeploy --env <environment>
```

This updates the ECS task definition and service, then waits for the deployment to stabilize (up to 20 minutes). ![f>][ji1o78hjrwit168fdiotuwop]

### CI/CD pipeline🔄

GitHub Actions automates the deployment process:

- **ingest.yml**: Runs typecheck and tests on the ingest package ![f>][hoxwk39njdnbnsc71jlntb8o]
- **ingest-docker.yml**: Builds and pushes Docker images when ingest files change ![f>][regux8tw4820i9i30t7fvcqq]
- **cd-ingest.yml**: Deploys to staging or production environments ![f>][x0ylc5kiaf1me505npkrateg]

## Monitoring📊

### Status tracking📈

The service maintains real-time counters for connector execution state:

- STATUS: Current execution state (INGESTING, COMPLETED, FAILED)
- TOTAL: Total number of items to process
- COMPLETED: Successfully processed items
- IN_PROGRESS: Currently processing items
- FAILED: Failed items ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Observability🔍

The service provides comprehensive monitoring:

- Structured JSON logs with correlation IDs and contextual metadata
- Metrics tracking message counts, processing latency, error rates, and queue depths
- Distributed tracing using OpenTelemetry
- Health check endpoints reporting service status and resource utilization
- Dashboards visualizing throughput, error rates, latency percentiles, and queue depths
- Alerts for error rate spikes, latency degradation, and queue backlog growth ![f>][ekkiwc3b9ivzit2wwgmlytfr]

### Performance characteristics⚡

- Processes up to 50,000 messages per second per instance
- Average end-to-end latency: 100ms for API submissions, 5 minutes for batch files
- Scales horizontally by adding instances behind load balancers
- Memory usage: 2GB average, 4GB maximum
- CPU utilization: 70% average target, 90% burst capacity ![f>][ekkiwc3b9ivzit2wwgmlytfr]

## Data quality💎

The service tracks quality metrics per source and data type:

- **Completeness**: Percentage of required fields populated
- **Accuracy**: Validation pass rate and business rule compliance
- **Timeliness**: Ingestion lag between source and processing timestamps
- **Consistency**: Detection of contradictions and duplicates

Quality alerts trigger when scores fall below 95% for critical data types. ![f>][ekkiwc3b9ivzit2wwgmlytfr]

## Security🔒

Security controls include:

- TLS 1.3 encryption for all network communications
- API key rotation every 90 days
- IP allowlisting for sensitive endpoints
- Request signing using HMAC-SHA256
- Audit logging of authentication attempts and data access
- Secrets management via HashiCorp Vault
- AES-256 encryption for data at rest ![f>][ekkiwc3b9ivzit2wwgmlytfr]