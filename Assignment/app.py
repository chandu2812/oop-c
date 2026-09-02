from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "hotel-reservation-secret-key"

# ==========================================
# 1. OOP HIERARCHY MIRRORING C++
# ==========================================
class HotelEntity:
    def __init__(self, entity_id="", name=""):
        self.entity_id = entity_id
        self.name = name

class RoomBase(HotelEntity):
    def __init__(self, entity_id="", name="", room_number=0):
        super().__init__(entity_id, name)
        self.room_number = room_number
        self.is_available = True

class AbstractRoom(RoomBase):
    def __init__(self, entity_id, name, room_number, base_rate):
        super().__init__(entity_id, name, room_number)
        self.base_rate = base_rate

    def calculate_tariff(self, nights):
        raise NotImplementedError("Pure virtual method")

    def get_category(self):
        raise NotImplementedError("Pure virtual method")

class StandardRoom(AbstractRoom):
    def __init__(self, room_number, base_rate=1200.0):
        super().__init__(f"STD-{room_number}", "Standard Room", room_number, base_rate)

    def calculate_tariff(self, nights):
        return self.base_rate * nights

    def get_category(self):
        return "Standard"

class DeluxeRoom(AbstractRoom):
    def __init__(self, room_number, base_rate=2800.0):
        super().__init__(f"DLX-{room_number}", "Deluxe Room", room_number, base_rate)

    def calculate_tariff(self, nights):
        return (self.base_rate + 500.0) * nights

    def get_category(self):
        return "Deluxe"

class SuiteRoom(AbstractRoom):
    def __init__(self, room_number, base_rate=6000.0):
        super().__init__(f"SUT-{room_number}", "Executive Suite", room_number, base_rate)

    def calculate_tariff(self, nights):
        return (self.base_rate + 2000.0) * nights

    def get_category(self):
        return "Executive Suite"

class Guest:
    def __init__(self, guest_id, name, phone):
        self.guest_id = guest_id
        self.name = name
        self.phone = phone

class Reservation:
    def __init__(self, res_id, guest_id, room_number, nights):
        self.res_id = res_id
        self.guest_id = guest_id
        self.room_number = room_number
        self.nights = nights
        self.is_active = True

# ==========================================
# 2. IN-MEMORY SYSTEM STATE
# ==========================================
rooms = [
    StandardRoom(101, 1200.0),
    StandardRoom(102, 1200.0),
    DeluxeRoom(201, 2800.0),
    DeluxeRoom(202, 2800.0),
    SuiteRoom(301, 6000.0)
]

guests = [
    Guest("G-101", "Aarav Sharma", "9876543210"),
    Guest("G-102", "Deepika Patel", "9123456780")
]

reservations = []
res_counter = 1001
last_invoice = None

# ==========================================
# 3. HTML UI TEMPLATE
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotel Reservation System - Flask Dashboard</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: var(--bg-color); color: var(--text-main); padding: 24px; line-height: 1.5; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 24px; border-bottom: 1px solid var(--card-border); padding-bottom: 16px; }
        header h1 { font-size: 1.8rem; margin-bottom: 6px; }
        header p { color: var(--text-muted); font-size: 0.95rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 20px; }
        .card h2 { font-size: 1.2rem; color: var(--accent); margin-bottom: 14px; }
        .form-group { margin-bottom: 12px; }
        label { display: block; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 4px; }
        input, select { width: 100%; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--card-border); background: #0f172a; color: var(--text-main); font-size: 0.9rem; outline: none; }
        button { width: 100%; padding: 10px; border-radius: 6px; border: none; background: var(--accent); color: white; font-weight: 600; font-size: 0.9rem; cursor: pointer; margin-top: 6px; }
        button:hover { background: var(--accent-hover); }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-top: 10px; }
        th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--card-border); }
        th { color: var(--text-muted); }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
        .badge-available { background: rgba(16, 185, 129, 0.2); color: var(--success); }
        .badge-occupied { background: rgba(239, 68, 68, 0.2); color: var(--danger); }
        .badge-confirmed { background: rgba(59, 130, 246, 0.2); color: var(--accent); }
        .badge-checkedout { background: rgba(148, 163, 184, 0.2); color: var(--text-muted); }
        .alert { padding: 10px 14px; border-radius: 6px; margin-bottom: 14px; font-size: 0.85rem; }
        .alert-success { background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid var(--success); }
        .alert-danger { background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid var(--danger); }
        .invoice-box { background: #090d16; border: 1px dashed var(--accent); border-radius: 8px; padding: 16px; margin-top: 16px; font-family: monospace; font-size: 0.85rem; }
        .invoice-line { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .divider { border-top: 1px dashed var(--card-border); margin: 8px 0; }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Hotel Reservation & Tariff Management System</h1>
        <p>Python Flask Application with Object-Oriented Polymorphic Engine</p>
    </header>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="grid">
        <!-- Room Inventory -->
        <div class="card">
            <h2>Room Inventory & Tariff</h2>
            <table>
                <thead>
                    <tr><th>Room</th><th>Category</th><th>Tariff/Night</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {% for r in rooms %}
                    <tr>
                        <td>#{{ r.room_number }}</td>
                        <td>{{ r.get_category() }}</td>
                        <td>INR {{ "%.2f"|format(r.calculate_tariff(1)) }}</td>
                        <td>
                            <span class="badge {{ 'badge-available' if r.is_available else 'badge-occupied' }}">
                                {{ 'Available' if r.is_available else 'Occupied' }}
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- Register Guest -->
        <div class="card">
            <h2>Register New Guest</h2>
            <form action="{{ url_for('register_guest') }}" method="POST">
                <div class="form-group">
                    <label>Guest ID</label>
                    <input type="text" name="guest_id" placeholder="e.g. G-103" required>
                </div>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" placeholder="e.g. Venkata Chandu" required>
                </div>
                <div class="form-group">
                    <label>Contact Phone</label>
                    <input type="text" name="phone" placeholder="e.g. 9876543210" required>
                </div>
                <button type="submit">Register Guest</button>
            </form>
        </div>

        <!-- Book Room -->
        <div class="card">
            <h2>Book a Room</h2>
            <form action="{{ url_for('book_room') }}" method="POST">
                <div class="form-group">
                    <label>Select Guest</label>
                    <select name="guest_id" required>
                        {% for g in guests %}
                        <option value="{{ g.guest_id }}">{{ g.name }} ({{ g.guest_id }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Select Available Room</label>
                    <select name="room_number" required>
                        {% for r in rooms if r.is_available %}
                        <option value="{{ r.room_number }}">Room #{{ r.room_number }} ({{ r.get_category() }} - INR {{ r.calculate_tariff(1) }}/nt)</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Duration of Stay (Nights)</label>
                    <input type="number" name="nights" value="2" min="1" required>
                </div>
                <button type="submit">Confirm Booking</button>
            </form>
        </div>

        <!-- Check Out & Invoice -->
        <div class="card">
            <h2>Check-Out & Billing</h2>
            <form action="{{ url_for('checkout_room') }}" method="POST">
                <div class="form-group">
                    <label>Select Active Reservation</label>
                    <select name="res_id" required>
                        {% for r in reservations if r.is_active %}
                        <option value="{{ r.res_id }}">{{ r.res_id }} - Room #{{ r.room_number }}</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit">Generate Invoice & Release Room</button>
            </form>

            {% if invoice %}
            <div class="invoice-box">
                <div style="text-align: center; font-weight: bold; margin-bottom: 8px;">--- HOTEL TAX INVOICE ---</div>
                <div class="invoice-line"><span>Invoice ID:</span><span>INV-{{ invoice.res_id }}</span></div>
                <div class="invoice-line"><span>Guest:</span><span>{{ invoice.guest_name }} ({{ invoice.guest_phone }})</span></div>
                <div class="invoice-line"><span>Room:</span><span>#{{ invoice.room_number }} ({{ invoice.category }})</span></div>
                <div class="invoice-line"><span>Duration:</span><span>{{ invoice.nights }} Night(s)</span></div>
                <div class="divider"></div>
                <div class="invoice-line"><span>Room Tariff:</span><span>INR {{ "%.2f"|format(invoice.tariff) }}</span></div>
                <div class="invoice-line"><span>GST (18%):</span><span>INR {{ "%.2f"|format(invoice.tax) }}</span></div>
                <div class="divider"></div>
                <div class="invoice-line" style="font-weight: bold; color: #10b981;"><span>Total Payable:</span><span>INR {{ "%.2f"|format(invoice.total) }}</span></div>
                <div style="text-align: center; margin-top: 8px; color: #94a3b8; font-size: 0.75rem;">Status: PAID IN FULL</div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- Reservations Table -->
    <div class="card">
        <h2>Active & Past Reservations</h2>
        <table>
            <thead>
                <tr><th>Res ID</th><th>Guest ID</th><th>Room</th><th>Nights</th><th>Status</th></tr>
            </thead>
            <tbody>
                {% for r in reservations %}
                <tr>
                    <td><strong>{{ r.res_id }}</strong></td>
                    <td>{{ r.guest_id }}</td>
                    <td>#{{ r.room_number }}</td>
                    <td>{{ r.nights }}</td>
                    <td>
                        <span class="badge {{ 'badge-confirmed' if r.is_active else 'badge-checkedout' }}">
                            {{ 'CONFIRMED' if r.is_active else 'CHECKED_OUT' }}
                        </span>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""

# ==========================================
# 4. ROUTING LOGIC
# ==========================================
@app.route('/')
def index():
    global last_invoice
    return render_template_string(HTML_TEMPLATE, rooms=rooms, guests=guests, reservations=reservations, invoice=last_invoice)

@app.route('/register_guest', methods=['POST'])
def register_guest():
    g_id = request.form.get('guest_id', '').strip()
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()

    if any(g.guest_id == g_id for g in guests):
        flash(f"Guest ID {g_id} already exists.", "danger")
    else:
        guests.append(Guest(g_id, name, phone))
        flash(f"Guest {name} registered successfully.", "success")
    return redirect(url_for('index'))

@app.route('/book_room', methods=['POST'])
def book_room():
    global res_counter
    g_id = request.form.get('guest_id')
    r_num = int(request.form.get('room_number', 0))
    nights = int(request.form.get('nights', 1))

    room = next((r for r in rooms if r.room_number == r_num and r.is_available), None)
    if not room:
        flash("Room is not available.", "danger")
        return redirect(url_for('index'))

    res_id = f"RES-{res_counter}"
    res_counter += 1
    reservations.append(Reservation(res_id, g_id, r_num, nights))
    room.is_available = False
    flash(f"Booking confirmed! Reservation ID: {res_id}", "success")
    return redirect(url_for('index'))

@app.route('/checkout_room', methods=['POST'])
def checkout_room():
    global last_invoice
    res_id = request.form.get('res_id')
    res = next((r for r in reservations if r.res_id == res_id and r.is_active), None)
    if not res:
        flash("Reservation not found or already closed.", "danger")
        return redirect(url_for('index'))

    room = next(r for r in rooms if r.room_number == res.room_number)
    guest = next((g for g in guests if g.guest_id == res.guest_id), None)

    tariff = room.calculate_tariff(res.nights)
    tax = tariff * 0.18
    total = tariff + tax

    res.is_active = False
    room.is_available = True

    last_invoice = {
        "res_id": res.res_id,
        "guest_name": guest.name if guest else res.guest_id,
        "guest_phone": guest.phone if guest else "N/A",
        "room_number": room.room_number,
        "category": room.get_category(),
        "nights": res.nights,
        "tariff": tariff,
        "tax": tax,
        "total": total
    }

    flash(f"Check-out complete for {res.res_id}. Room #{room.room_number} released.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)