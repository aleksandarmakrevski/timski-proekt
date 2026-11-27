import { useEffect, useState } from "react";
import { Link, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import api from "./api";

function Layout({ children }) {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  useEffect(() => {
    if (localStorage.getItem("access")) api.get("/auth/me/").then(r => setUser(r.data)).catch(() => {
      localStorage.removeItem("access"); localStorage.removeItem("refresh");
    });
  }, []);
  function logout() {
    localStorage.removeItem("access"); localStorage.removeItem("refresh");
    setUser(null); navigate("/");
  }
  return <><header><Link className="brand" to="/">GRAND HOTEL</Link><nav>
    <Link to="/">Home</Link><Link to="/hotel-info">Hotel Info</Link><Link to="/booking">Booking</Link><Link to="/contact">Contact</Link>
    {user ? <><Link to="/my-reservations">My reservations</Link><button className="link-button" onClick={logout}>Logout</button></> : <><Link to="/login">Login</Link><Link to="/register">Register</Link></>}
    <a href="http://127.0.0.1:8000/admin/" target="_blank" rel="noreferrer">Employee Admin</a>
  </nav></header><main>{children}</main><footer>Grand Hotel · Hotel Management System</footer></>;
}
function Home() {
  return <section className="hero"><div><p className="eyebrow">WELCOME TO GRAND HOTEL</p><h1>A comfortable stay,<br/>thoughtfully designed.</h1><p>Discover our rooms, explore hotel facilities and book your stay.</p><Link className="primary" to="/booking">Explore rooms</Link></div></section>;
}
function HotelInfo() {
  const [hotel, setHotel] = useState(null);
  const [sponsors, setSponsors] = useState([]);
  useEffect(() => { api.get("/hotel/").then(r => setHotel(r.data[0] || null)); api.get("/hotel/sponsors/").then(r => setSponsors(r.data)); }, []);
  return <section className="container"><h1>Hotel Information</h1>{hotel ? <><h2>{hotel.name}</h2><p>{hotel.description}</p><h2>Our history</h2><p>{hotel.history}</p><p>{hotel.address}</p></> : <p>Hotel information will be published here.</p>}<h2>Our sponsors</h2><div className="grid">{sponsors.map(s => <article className="card" key={s.id}><h3>{s.name}</h3><p>{s.description}</p></article>)}</div></section>;
}
function Booking() {
  const [rooms, setRooms] = useState([]);
  const [filters, setFilters] = useState({check_in:"",check_out:"",min_price:"",max_price:"",beds:"",floor:"",view:""});
  const [message, setMessage] = useState("");
  async function search(e) {
    e?.preventDefault(); setMessage("");
    const params = Object.fromEntries(Object.entries(filters).filter(([,v]) => v !== ""));
    try { const r = await api.get("/rooms/", {params}); setRooms(r.data); }
    catch { setMessage("Could not load rooms. Please try again."); }
  }
  useEffect(() => { search(); }, []);
  function update(e) { setFilters({...filters,[e.target.name]:e.target.value}); }
  async function reserve(room) {
    if (!localStorage.getItem("access")) { setMessage("Please log in before making a reservation."); return; }
    const check_in = filters.check_in, check_out = filters.check_out;
    if (!check_in || !check_out) { setMessage("Select check-in and check-out dates first."); return; }
    const guests = window.prompt("Number of guests:", "1");
    if (!guests) return;
    try {
      await api.post("/reservations/", {room:room.id,check_in,check_out,guests:Number(guests)});
      setMessage("Reservation request created successfully."); search();
    } catch (err) { setMessage(err.response?.data?.detail || "Reservation could not be created."); }
  }
  return <section className="container"><h1>Find your room</h1><form className="filters" onSubmit={search}>
    <label>Check-in<input type="date" name="check_in" value={filters.check_in} onChange={update}/></label>
    <label>Check-out<input type="date" name="check_out" value={filters.check_out} onChange={update}/></label>
    <label>Min price<input type="number" name="min_price" value={filters.min_price} onChange={update}/></label>
    <label>Max price<input type="number" name="max_price" value={filters.max_price} onChange={update}/></label>
    <label>Beds<input type="number" min="1" name="beds" value={filters.beds} onChange={update}/></label>
    <label>Floor<input type="number" min="0" name="floor" value={filters.floor} onChange={update}/></label>
    <label>View<select name="view" value={filters.view} onChange={update}><option value="">Any view</option><option value="sea">Sea</option><option value="city">City</option><option value="garden">Garden</option><option value="mountain">Mountain</option><option value="other">Other</option></select></label>
    <button className="primary">Search rooms</button>
  </form>{message && <p className="notice">{message}</p>}<div className="grid">{rooms.map(room => <article className="card" key={room.id}><div className="room-placeholder">ROOM {room.number}</div><div className="card-body"><p className="eyebrow">{room.room_type_name}</p><h2>{room.price_per_night} € <small>/ night</small></h2><p>{room.description || "Comfortable hotel room."}</p><p>{room.beds} beds · Floor {room.floor} · {room.capacity} guests · {room.view} view</p><button className="primary" onClick={() => reserve(room)}>Book this room</button></div></article>)}</div>{rooms.length===0 && <p>No rooms found. Add rooms through Django Admin.</p>}</section>;
}
function Contact() {
  const [form,setForm] = useState({name:"",email:"",subject:"",message:""});
  const [result,setResult] = useState("");
  async function submit(e) { e.preventDefault(); try { await api.post("/contact/",form); setResult("Your message has been sent."); setForm({name:"",email:"",subject:"",message:""}); } catch { setResult("Message could not be sent. Check the entered information."); } }
  return <section className="container narrow"><h1>Contact us</h1><form className="stack" onSubmit={submit}>{["name","email","subject","message"].map(k => <label key={k}>{k==="message"?"Message":k[0].toUpperCase()+k.slice(1)}{k==="message"?<textarea required value={form[k]} onChange={e=>setForm({...form,[k]:e.target.value})}/>:<input required={k!=="subject"} type={k==="email"?"email":"text"} value={form[k]} onChange={e=>setForm({...form,[k]:e.target.value})}/>}</label>)}<button className="primary">Send message</button></form>{result && <p className="notice">{result}</p>}<h2>Find us</h2><p>Add the hotel's Google Maps embed URL in Hotel Information through Django Admin.</p></section>;
}
function Auth({register=false}) {
  const [form,setForm]=useState({username:"",password:"",email:"",first_name:"",last_name:""});
  const [error,setError]=useState(""); const navigate=useNavigate();
  async function submit(e) { e.preventDefault(); setError(""); try {
    if(register) await api.post("/auth/register/",form);
    const r=await api.post("/auth/login/",{username:form.username,password:form.password});
    localStorage.setItem("access",r.data.access); localStorage.setItem("refresh",r.data.refresh); navigate("/");
  } catch(err) { setError(JSON.stringify(err.response?.data || "Authentication failed.")); } }
  return <section className="container narrow"><h1>{register?"Create account":"Login"}</h1><form className="stack" onSubmit={submit}>
    {register && <><label>Email<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/></label><label>First name<input value={form.first_name} onChange={e=>setForm({...form,first_name:e.target.value})}/></label><label>Last name<input value={form.last_name} onChange={e=>setForm({...form,last_name:e.target.value})}/></label></>}
    <label>Username<input required value={form.username} onChange={e=>setForm({...form,username:e.target.value})}/></label><label>Password<input type="password" required minLength="8" value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/></label><button className="primary">{register?"Register":"Login"}</button></form>{error && <p className="notice">{error}</p>}</section>;
}
function MyReservations() {
  const [items,setItems]=useState([]); const [error,setError]=useState("");
  useEffect(()=>{api.get("/reservations/").then(r=>setItems(r.data)).catch(()=>setError("Please log in to view your reservations."));},[]);
  return <section className="container"><h1>My reservations</h1>{error && <p>{error}</p>}{items.map(x=><article className="card reservation" key={x.id}><h3>Reservation #{x.id} · Room {x.room_number}</h3><p>{x.check_in} – {x.check_out}</p><p>Status: {x.status} · Total: {x.total_price} €</p></article>)}</section>;
}
export default function App() {
  return <Layout><Routes><Route path="/" element={<Home/>}/><Route path="/hotel-info" element={<HotelInfo/>}/><Route path="/booking" element={<Booking/>}/><Route path="/contact" element={<Contact/>}/><Route path="/login" element={<Auth/>}/><Route path="/register" element={<Auth register/>}/><Route path="/my-reservations" element={<MyReservations/>}/><Route path="*" element={<Navigate to="/"/>}/></Routes></Layout>;
}
