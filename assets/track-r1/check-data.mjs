// Optional offline reviewer CLI; no network, no edits to input.
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {analyze} from './geometry-core.mjs';
if(!process.argv[2]){console.error('Usage: node check-data.mjs path-to-survey-exchange.json');process.exit(2);}
try{
 const raw=await readFile(process.argv[2]);const result=analyze(JSON.parse(raw.toString('utf8')));
 result.calculated_utc=new Date().toISOString();
 result.input_sha256=createHash('sha256').update(raw).digest('hex');
 process.stdout.write(JSON.stringify(result,null,2)+'\n');
 if(result.data_quality==='invalid')process.exitCode=1;
}catch(e){console.error('No analysis issued: '+e.message);process.exitCode=2;}
