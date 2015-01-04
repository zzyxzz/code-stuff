package FindDistance;
import java.io.*;
import java.util.Arrays;


public class FindLtLg {
	static final String csvFile     = "postcodes.csv";
	static final String cvsSplitBy  = ",";
	
	String[] postcode = new String[] {"CT2 7NZ","CT1 2DJ","ME4 3RJ","ME4 4AG","ME7 2HN"};//given postcodes for calculation
	double[] lt = new double[postcode.length];
	double[] lg = new double[postcode.length];
	
	String line = "";
	BufferedReader br = null;
	
	//read csvfile of the postcode data
	public FindLtLg(){
		try {
			br = new BufferedReader(new FileReader(csvFile));
			System.out.println("reader ready");
		}
		catch(FileNotFoundException e){
			e.printStackTrace();
		}
	}
	
	//search the given postcodes from postcodes data file
	//add corresponding longitude and latitude to lg and lt lists
	public void searchCode(){
		String[] codeFrom = getSortedCode();
		try{
			for(int i = 0; i < codeFrom.length; i++){
				boolean find = false;
				while(!find && ((line = br.readLine())!=null)){
					String[] gridInfo = line.split(cvsSplitBy);
										
					if(gridInfo[0].equals(codeFrom[i])) {
						lt[i] = Double.parseDouble(gridInfo[1]);
						lg[i] = Double.parseDouble(gridInfo[2]);
						find = true;
						//System.out.println("found");
						
					}
				}
			}
		}
		catch(IOException e){
			e.printStackTrace();
		}
	}
	
	//return latitude list
	public double[] getLt(){
		return lt;
	}
	
	//return longitude list
	public double[] getLg(){
		return lg;
	}
	
	//sort given postcode
	public String[] getSortedCode(){
		Arrays.sort(postcode);
		return postcode;
	}

}
