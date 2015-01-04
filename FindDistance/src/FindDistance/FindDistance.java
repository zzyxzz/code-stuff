package FindDistance;

import java.util.HashMap;

public class FindDistance {
	

	public static void main(String[] args) {
	
		double distance = 0;
		HashMap<String,String> hash = new HashMap<String,String>();
		
		FindLtLg ltlg = new FindLtLg();
		String[] code = ltlg.getSortedCode();
		ltlg.searchCode();
		
		double[] lt = ltlg.getLt();
		double[] lg = ltlg.getLg();
		
		for(int i = 0; i < code.length-1; i++) {   //iterating given postcods
			for(int t = i+1; t < code.length; t++) {
				double ltdiff = Math.toRadians(lt[i]-lt[t]); //latitude difference
				double lgdiff = Math.toRadians(lg[i]-lg[t]); //longitude difference
				double lt1 = Math.toRadians(lt[i]);		//convert to radians
				double lt2 = Math.toRadians(lt[t]);
				
				//haversine formula to calculate distance between two points
				double haversine  = Math.pow(Math.sin(ltdiff/2),2) + Math.cos(lt1)*Math.cos(lt2)*Math.pow(Math.sin(lgdiff)/2, 2);
				double formu = 2*Math.atan2(Math.sqrt(haversine), Math.sqrt(1-haversine));
				distance = 6371 * formu;
				String path = "From " + code[i] + " to " + code[t];
				String dis =  " is " + distance + " Km";
				hash.put(path,dis);
			}
		}
		
		//print results
		for(String key: hash.keySet()){
			System.out.println(key + hash.get(key) );
		}
	}
					
}
