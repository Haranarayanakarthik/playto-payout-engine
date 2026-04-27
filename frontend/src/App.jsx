import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [balance, setBalance] = useState(0);
  const [payouts, setPayouts] = useState([]);
  const [amount, setAmount] = useState(5000);

  const fetchData = async () => {
    const res = await axios.get("http://localhost:8000/api/v1/dashboard");
    setBalance(res.data.balance);
    setPayouts(res.data.payouts);
  };

 const createPayout = async () => {
   console.log("BUTTON CLICKED"); // 👈 IMPORTANT

   try {
     const res = await axios.post(
       "http://localhost:8000/api/v1/payouts",
       { amount_paise: amount },
       {
         headers: {
           "Idempotency-Key": crypto.randomUUID(),
         },
       },
     );

     console.log("SUCCESS:", res.data);

     await fetchData();
   } catch (err) {
     console.error("ERROR:", err);
   }
 };

  useEffect(() => {
    fetchData();
    const i = setInterval(fetchData, 3000);
    return () => clearInterval(i);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Balance: ₹{balance / 100}</h2>

      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
      />

      <button
        onClick={() => {
          alert("clicked");
          createPayout();
        }}
      >
        Create Payout
      </button>

      <h3>Payouts</h3>
      {payouts.map((p) => (
        <div key={p.id}>
          #{p.id} - ₹{p.amount_paise / 100} - {p.status}
        </div>
      ))}
    </div>
  );
}
