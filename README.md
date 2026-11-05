# Healthcare & Pharmaceutical Database Management System

A comprehensive relational database project built with **MySQL (8.0.39)**, **Python**, and **Pandas**. This project models clinical workflows, automated adverse drug interaction alerts, supply-chain contract economics, and pharmacy fulfillment metrics.

---

## 📌 Project Overview

In healthcare informatics, data integrity and automated safety checks are critical. This project implements an end-to-end relational database system designed to:
- Enforce relational integrity across patients, physicians, pharmacies, drugs, and manufacturers.
- Automate patient safety monitoring via a **MySQL trigger** that detects hazardous drug interactions upon prescription entry.
- Perform complex analytics (cost markup analysis, fulfillment turnaround times, physician prescribing trends) using advanced SQL (CTEs, temporal functions, windowing techniques).

---

## 🏗️ Architecture & Schema Design

The database conforms to Third Normal Form (3NF) to minimize redundancy and prevent update/delete anomalies:

- **Entity Tables**:
  - `physicians`: SSN (PK), name, specialty, years of experience.
  - `patients`: SSN (PK), demographics, primary care physician FK.
  - `pharmacies`: ID (PK), name, address, phone.
  - `drugs`: Drug name (PK), formula.
  - `companies`: ID (PK), pharmaceutical manufacturer name, contact info.
- **Transactional & Relationship Tables**:
  - `prescriptions`: Prescribing physician, patient, drug, dosage, and date.
  - `pharmacy_fills`: Dispensation events, fulfillment timestamp, quantity, and retail price.
  - `contracts`: Wholesale supply contracts between manufacturers and pharmacies.
  - `adverse_interactions`: Documented contraindications between drug pairs.
  - `alerts`: System-generated flags populated automatically by database triggers.

*(Entity Relationship Diagrams are available in [`diagram/Medical Database EER.pdf`](diagram/Medical%20Database%20EER.pdf)).*

---

## ⚡ Automated Safety Logic (Trigger)

The database includes an active safety trigger:
- **`alert_addition` (`AFTER INSERT ON prescriptions`)**: Evaluates whether the incoming medication interacts with any prior prescription for that patient. If a contraindication exists in `adverse_interactions`, an alert record is immediately written to `alerts` linking the patient, prescribing physician, and conflicting drugs.

---

## 🔍 Analytical Business Queries

The project implements solutions to key clinical and business questions:

1. **High-Risk Prescribing Analysis**: Identifies physicians who generated the highest count of adverse drug interaction alerts using CTEs and subquery aggregations.
2. **Co-Prescription Contraindications**: Flags physicians who prescribed conflicting drug pairs to the same individual patient.
3. **Manufacturer Volume**: Ranks physicians who prescribe the highest volume of medications manufactured by specific pharmaceutical suppliers.
4. **Wholesale vs. Retail Price Spread**: Compares manufacturer contract prices against market-wide pharmacy retail prices for targeted drugs.
5. **Pharmacy Markup Percentage**: Calculates the exact retail margin markup percentage per drug across dispensing pharmacies.
6. **Prescription Turnaround Lead Time**: Computes average elapsed time (in hours/days) from prescription issuance to pharmacy fulfillment using MySQL date/time arithmetic (`TIMESTAMPDIFF`).
7. **Unfilled Prescription Audit**: Pinpoints prescriptions that were authorized but never filled at designated pharmacies.

---

## 🚀 Getting Started

### Prerequisites
- **MySQL Server 8.0+**
- **Python 3.9+**
- Python Packages:
  ```bash
  pip install mysql-connector-python pandas
  ```

### Configuration & Security Best Practice
To keep database credentials secure when publishing code to GitHub, avoid hardcoding passwords directly into the notebook. You can pass your credentials via environment variables or a local `.env` file:
```bash
export MYSQL_PASSWORD="your_password_here"
```
Or use Python's `getpass` module for an interactive prompt during notebook execution.

### Running the Notebook
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/medical-database-project.git
   cd medical-database-project
   ```
2. Open [`src/SQLProject.ipynb`](src/SQLProject.ipynb).
3. Run the cells sequentially to initialize the schema (`medical_database`), populate data from `data/*.csv`, deploy the triggers, and execute the analytical queries.
