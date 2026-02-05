
# Architecture — Web Service

## 1. Service Positioning

### 1.1 Service Position within the System

- This service is one of the components of the Market Data Platform and serves as the **official data delivery boundary**.
- This service is not the core of the system and is not responsible for data production, analysis, or modification.
- Removing this service does not result in data loss or disruption of upstream processes.

---
### 1.2 System State Before the Web Service

- Prior to this service, market data:
  - was collected,
  - standardized,
  - and stored in the system database.
- However, there was no official, stable, and controlled interface for external consumption.
- The creation of this service is a targeted response to this specific gap.

---
### 1.3 Source of Truth and Service Inputs

- The sole input source of this service is the data stored in the system database.
- All data is converted into the system’s unified canonical format before reaching this service.
- This service performs no interpretive processing, mapping, transformation, or decision-making on the data.

---

### 1.4 Shared Language with Consumers

- The web service language is the same as the system’s unified data language.
- The exposed concepts directly reflect the system’s internal concepts.
- The web service does not act as a translator or re-definition layer.

---
### 1.5 Scope of Deliverable Data

- This service does not guarantee full coverage of all possible data.
- Only data explicitly marked as supported in upstream systems is exposed.
- The supported or unsupported status of any data must be transparently communicated to the consumer.

---
### 1.6 Role of the Web Service in the Consumption Flow

- This service is the official interface of the system for external consumers.
- It does not act as a decision-maker or as a place for business or analytical logic.
- The growth of this service is defined solely in terms of consumption volume and quality.

---
## 2. Problem Statement

Market data within the system is stored in a structured, unified, and reliable manner, but lacks an official and stable layer for external consumption. The absence of such a boundary makes external access either impossible or fragmented and dependent on ad-hoc implementations—an approach incompatible with a sustainable, data-driven system. The core problem is the lack of an independent layer that provides official, controlled, and neutral access to stored unified data for external consumers.

---

## 3. Goals

- Establish an official and stable pathway for external access to unified system data
- Preserve the full meaning and structure of data without interpretation or redefinition
- Fully separate the data consumption layer from data production and maintenance processes
- Provide a controlled consumption platform without introducing analytical or decision-making logic

---

## 4. Out of Scope

- Production, synchronization, or modification of market data
- Analysis, aggregation, or derived computations on data
- Decision-making, forecasting, or signal generation
- Guaranteeing full coverage of all markets, symbols, or time intervals
- Providing user interfaces or consumer-facing tools

---

## 5. Service Responsibilities

- Official and stable delivery of supported system data
- Reflecting data status without interfering with selection or decision logic
- Acting as the boundary between external consumers and the system’s data core
- Identifying consumers and associating each request with a specific consumer
- Supporting two classes of consumers:
  - Public consumers with limited access (identified by IP)
  - Registered consumers with key-based access
- Enforcing consumption control policies and generating data required for monitoring and reporting
- Providing official documentation as part of the service output
- Allowing access and consumption policies to be applied at the access-key level

---

## 6. Trust and Responsibility Boundaries

- Data correctness, integrity, and freshness are the responsibility of upstream systems.
- Lack of data or unsupported data coverage is not considered a service error.
- This service is responsible for transparent reporting of states and errors, not for guaranteeing data quality.
- Every request must be attributable to a consumer (public or registered).
- The service must allow defining, managing, and disabling independent access keys for a single registered consumer without impacting other keys.
- Technical details of access, consumption, and reporting policies are defined in the technical design phase.
- The service must be designed so that the following reports can be extracted without architectural changes:
  - Consumption at both consumer and key levels
  - Request rate, volume, and usage patterns
  - Errors and response statuses per consumer
  - Security and control events (rate limiting, blocking)

---

## 7. Service Evolution Direction

- Permitted evolution is limited to improvements in access policies, consumption control, monitoring, reporting, and developer experience.
- Introducing analytical, aggregative, or decision-making logic is outside the allowed evolution path.
- Defining consumption tiers and plans is permitted, provided the boundary-neutral nature of the service is preserved.

---

## 8. Open Architectural Questions

- Precise definition of public consumer identification policy alongside registered consumers
- Definition of consumption tiering policies and their relationship to usage limits and measurement
- Minimum metrics and events required for monitoring, reporting, and debugging
- Contract versioning policy and handling of breaking changes in the future
