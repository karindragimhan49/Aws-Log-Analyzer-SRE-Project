# Automated AWS Log Analyzer & Resiliency Framework

![Project Architecture Diagram](https://github.com/karindragimhan49/Aws-Log-Analyzer-SRE-Project/blob/5c05e94341e3156fee84e7e4f428b9f002d5cfa0/snap/digram.png)

## 🚀 Overview

This project is a hands-on implementation of a TechOps/SRE (Site Reliability Engineering) solution built entirely on AWS. It demonstrates a complete, end-to-end pipeline for log generation, centralized storage, automated analysis, real-time monitoring, and self-healing. The primary goal is to simulate a production environment where system stability and reliability are maintained through automation, aligning with the core responsibilities of an L2 Production Support or TechOps role.

This project was developed to showcase practical skills in cloud computing (AWS), scripting (Python, Bash), monitoring, and SRE principles as outlined in the TechOps Intern job description.

---

## ✨ Key Features & Job Description Alignment

| Feature | JD Responsibility Covered | Tools & Technologies Used |
| :--- | :--- | :--- |
| **Log Generation & Collection** | _(Implicit)_ System Operation | `Python`, `EC2` -> `S3` |
| **Automated Log Analysis** | Analyze system logs, Root Cause Analysis | `Python (Boto3)`, `S3` |
| **Real-time Monitoring & Dashboards**| Monitor application performance, Create dashboards | `CloudWatch Metrics`, `CloudWatch Dashboards` |
| **Incident Alerting** | Investigate and troubleshoot incidents and system alerts | `CloudWatch Alarms`, `Amazon SNS` (Email) |
| **Automated Self-Healing** | Identify recurring issues, Propose automation, Write scripts | `Bash Script`, `Linux Cronjob`, `EC2` |
| **Documentation & Version Control** | Document troubleshooting steps, SOPs | `Git`, `GitHub`, `Markdown` |

---

## 🏛️ Architecture Diagram

The system is composed of several AWS services working in tandem to create a robust and automated pipeline.

*(Your diagram will go here)*

**Workflow:**
1.  **Log Generation:** A Python script (`log_generator.py`) runs on an **Amazon EC2** instance, simulating application logs (INFO, WARNING, ERROR).
2.  **Centralized Storage:** These log files are periodically uploaded to a dedicated **Amazon S3** bucket.
3.  **Log Analysis:** A second Python script (`log_analyzer.py`) continuously polls the S3 bucket for new logs. It processes each file, identifying lines with "ERROR" or "CRITICAL" keywords.
4.  **Metric Publication:** The analyzer script calculates the number of errors and publishes this value as a custom metric (`ErrorCount`) to **Amazon CloudWatch** under the `LogAnalyzerApp` namespace.
5.  **Monitoring & Alerting:**
    *   A **CloudWatch Dashboard** provides a real-time visual representation of the `ErrorCount` metric.
    *   A **CloudWatch Alarm** monitors this metric. If the error count exceeds a predefined threshold (e.g., > 5 errors per minute), it triggers an **Amazon SNS** notification, sending an alert email to the support team.
6.  **Self-Healing:** A Bash script (`process_monitor.sh`), scheduled as a **Linux Cronjob**, runs every 5 minutes on the EC2 instance. It checks if the critical `log_analyzer.py` process is running. If not, it automatically restarts the process and logs the action, ensuring high availability.

---

## 🛠️ Tech Stack

*   **Cloud Provider:** AWS (Amazon Web Services)
*   **Core AWS Services:**
    *   `EC2 (Amazon Linux 2023)`: Virtual server for running our scripts.
    *   `S3`: Scalable storage for log files.
    *   `CloudWatch`: For metrics, dashboards, and alarms.
    *   `IAM`: Securely managed access for the EC2 instance.
    *   `SNS`: For sending email alerts.
*   **Scripting Languages:**
    *   `Python 3`: For log generation and analysis (using the `boto3` SDK).
    *   `Bash`: For the automated self-healing script.
*   **CI/CD & Version Control:** `Git`, `GitHub`
*   **Orchestration:** `Linux Cron` for task scheduling.

---

## 📸 Project Screenshots

### CloudWatch Monitoring Dashboard
*A real-time view of the error count, providing instant visibility into system health.*
![CloudWatch Dashboard](https://github.com/karindragimhan49/Aws-Log-Analyzer-SRE-Project/blob/5c05e94341e3156fee84e7e4f428b9f002d5cfa0/snap/cloudwatch.png)

### Self-Healing in Action
*The log file of the process monitor, showing that it detected a crashed process and automatically restarted it.*
![Process Monitor Log](https://github.com/karindragimhan49/Aws-Log-Analyzer-SRE-Project/blob/5c05e94341e3156fee84e7e4f428b9f002d5cfa0/snap/Aws%20ec2%20.png)

---

## ⚙️ How to Run

1.  **Prerequisites:**
    *   An AWS Account with appropriate permissions.
    *   Git installed on your local machine.
    *   AWS CLI configured (optional).

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/[your-username]/[your-repo-name].git
    cd [your-repo-name]
    ```

3.  **Setup AWS Infrastructure:**
    *   Create an S3 bucket.
    *   Create an IAM Role for EC2 with `S3FullAccess` and `CloudWatchFullAccess` permissions.
    *   Launch an EC2 instance (Amazon Linux 2023, t2.micro) with the created IAM Role.
    *   Update the `S3_BUCKET_NAME` in `log_generator.py` and `log_analyzer.py`.
    *   Update the `PROJECT_DIR` path in `process_monitor.sh` if necessary.

4.  **Deploy and Run:**
    *   SSH into the EC2 instance.
    *   Clone the repository onto the instance.
    *   Run the `log_generator.py` in one terminal session.
    *   Run the `log_analyzer.py` in another session to start the analysis.
    *   Set up the `process_monitor.sh` as a cronjob for self-healing.
