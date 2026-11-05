import { Pool } from 'pg';
import { timingSafeEqual } from 'node:crypto';
const pool=new Pool({connectionString:process.env.ECHO_TICK_DATABASE_URL,max:1,ssl:{rejectUnauthorized:true}});
function authorized(req){
 const expected=process.env.CRON_SECRET,provided=req.headers.authorization?.replace(/^Bearer /i,'');
 if(!expected||!provided)return false;
 const a=Buffer.from(provided),b=Buffer.from(expected);
 return a.length===b.length&&timingSafeEqual(a,b);
}
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='GET')return res.status(405).json({error:'method_not_allowed'});
 if(!authorized(req))return res.status(401).json({error:'unauthorized'});
 try{
  const result=await pool.query('SELECT echo_warehouse.apply_entropy_tick() AS tick');
  return res.status(200).json({tick:result.rows[0].tick});
 }catch(err){console.error('entropy tick failed',err.code||err.name);return res.status(503).json({error:'entropy_unavailable'});}
}
