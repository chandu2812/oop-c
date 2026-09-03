# Hotel Accommodation and Reservation Management System (C++)

An object-oriented C++ software system engineered to manage room inventories, guest lifecycles, real-time availability tracking, polymorphic tariff aggregation, and digital invoicing.

---

## 📌 Project Overview & Problem Formulation
The **Hotel Accommodation and Reservation Management System** addresses inefficiencies in manual room booking and billing. By utilizing modern Object-Oriented Programming (OOP) paradigms in C++17, the system models real-world hotel operations with high modularity, extensible pricing architectures, memory safety, and paperless tax invoice generation.

### Key Objectives
* Enforce room reservation integrity and eliminate double-booking.
* Provide dynamic pricing calculations through runtime polymorphism.
* Eliminate diamond inheritance ambiguity using virtual base classes.
* Offer a menu-driven interface with structured data modeling.

---

## ⚙️ Relevant OOP Concepts Applied

1. **Virtual Base Classes & Diamond Resolution:**
   `HotelEntity` serves as a virtual base class for `RoomBase` and `ServiceBase` (`virtual public HotelEntity`). This eliminates data duplication and reference ambiguity when combined package entities inherit from both.
2. **Abstract Classes & Pure Virtual Interfaces:**
   `AbstractRoom` defines pure virtual methods (`calculateTariff()`, `displayDetails()`, `getCategory()`), enforcing strict interface contracts for derived room categories.
3. **Runtime Polymorphism via Base Class Pointers:**
   Heterogeneous room collections are stored as base pointers (`AbstractRoom*` via `std::unique_ptr<AbstractRoom>`). At runtime, calling `calculateTariff()` executes the corresponding derived override (`StandardRoom`, `DeluxeRoom`, `SuiteRoom`) dynamically via the virtual table (`vtable`).
4. **Encapsulation & Data Hiding:**
   Entity attributes (tariffs, availability flags, guest identification) are protected and exposed only through validated public accessors and mutators.
5. **Modern Memory Safety:**
   Dynamic memory allocations are wrapped in `std::unique_ptr` and `std::make_unique` to prevent memory leaks without manual destruction.

---

## 🏨 Room Hierarchy & Dynamic Tariff Rules

| Room Type | Base Rate / Night | Key Amenities | Tariff Calculation Rule |
| :--- | :--- | :--- | :--- |
| **Standard Room** | INR 1,200 | Complimentary Wi-Fi, Desk | `BaseRate × Nights` |
| **Deluxe Room** | INR 2,800 | Sea View, Mini-Bar | `(BaseRate + 500) × Nights` |
| **Executive Suite** | INR 6,000 | Jacuzzi, Butler Service | `(BaseRate + 2000) × Nights` |

* **Taxes:** Applied automatically at checkout as 18% GST on the subtotal.

---
---
