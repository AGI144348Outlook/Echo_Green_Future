import { Pool } from 'pg';
import { timingSafeEqual } from 'node:crypto';
const pool = new Pool({ connectionString: process.env.ECHO_AGENT_DATABASE_URL, max: 2, ssl: { rejectUnauthorized: true } });
function authorized(req) {
 const expected=process.env.ECHO_API_TOKEN;
 const provided=req.headers.authorization?.replace(/^Bearer /i,'');
 if(!expected||!provided) return false;
 const a=Buffer.from(provided),b=Buffer.from(expected);
 return a.length===b.length && timingSafeEqual(a,b);
}
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(!authorized(req)) return res.status(401).json({error:'unauthorized'});
 try{
  if(req.method==='GET'){
   const [boxes,ties]=await Promise.all([
    pool.query('SELECT box_id,generation,payload,accessibility,created_tick FROM echo_warehouse.accessible_boxes ORDER BY box_id DESC LIMIT 100'),
    pool.query('SELECT tie_id,from_box,to_box,relation,strength,phase FROM echo_warehouse.accessible_ties ORDER BY tie_id DESC LIMIT 200')
   ]);
   return res.status(200).json({boxes:boxes.rows,ties:ties.rows});
  }
  if(req.method==='POST'){
   const {kind,id,amount=0.10}=req.body||{};
   if(!['box','tie'].includes(kind)||!Number.isSafeInteger(id)||id<1||typeof amount!=='number'||amount<=0||amount>0.10) return res.status(400).json({error:'invalid_request'});
   const result=await pool.query('SELECT echo_warehouse.reinforce($1,$2,$3) AS maintained',[kind,id,amount]);
   return res.status(200).json({maintained:result.rows[0].maintained});
  }
  res.setHeader('Allow','GET, POST');return res.status(405).json({error:'method_not_allowed'});
 }catch(err){console.error('warehouse request failed',err.code||err.name);return res.status(503).json({error:'warehouse_unavailable'});}
}
