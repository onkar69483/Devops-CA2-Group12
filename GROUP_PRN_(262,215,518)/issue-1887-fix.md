# ✅ Issue Fix Report: #1887

**🔹 Group Name**: [Group No: 24,25,26]  
**🔹 Problem Statement**: Issue #1887 from testcontainers/testcontainers-java

---

## 🛠️ Description of the Issue

The method `getR2dbcUrl()` was not returning the correct connection string for PostgreSQL containers. It missed formatting or required credentials, making it incompatible with R2DBC clients.

---

## ✅ How I Fixed It

- Located the source file where `getR2dbcUrl()` was defined.
- Reconstructed the method to return the correct R2DBC format:
  
