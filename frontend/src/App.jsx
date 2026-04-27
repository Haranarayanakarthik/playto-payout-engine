import { useEffect, useState } from "react";
import axios from "axios";

// 🔥 Use deployed backend URL
const API = "https://playto-payout-engine-gqld.onrender.com";

export default function App() {
  const [balance, setBalance] = useState(0);
  const [payouts, setPayouts] = useState([]);
  const [amount, setAmount] = useState(5000);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const res = await axios.get(`${API}/api/v1/dashboard`);
      setBalance(res.data.balance);
      setPayouts(res.data.payouts);
    } catch (err) {
      console.error("FETCH ERROR:", err);
    }
  };

  const createPayout = async () => {
    console.log("BUTTON CLICKED");

    try {
      setLoading(true);

      const res = await axios.post(
        `${API}/api/v1/payouts`,
        { amount_paise: amount },
        {
          headers: {
            "Idempotency-Key": crypto.randomUUID(),
          },
        }
      );

      console.log("SUCCESS:", res.data);

      await fetchData();
    } catch (err) {
      console.error("ERROR:", err);
      alert("Payout failed (check console)");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    const i = setInterval(fetchData, 5000); // reduce spam
    return () => clearInterval(i);
  }, []);

  return (
    <div style={{ padding: 20, maxWidth: 500, margin: "auto" }}>
      <h2>Balance: ₹{balance / 100}</h2>

      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
        style={{ marginRight: 10 }}
      />

      <button onClick={createPayout} disabled={loading}>
        {loading ? "Processing..." : "Create Payout"}
      </button>

      <h3 style={{ marginTop: 20 }}>Payouts</h3>

      {payouts.length === 0 && <p>No payouts yet</p>}

      {payouts.map((p) => (
        <div key={p.id}>
          #{p.id} - ₹{p.amount_paise / 100} - {p.status}
        </div>
      ))}
    </div>
  );
}
