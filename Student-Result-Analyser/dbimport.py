from tabula import read_pdf
import mysql.connector
import sys

def read_table(page):
    try:
        dfs = read_pdf(pdf_path, pages=str(page))
        if not dfs:
            print("ERROR!!!")
            return None
        elif(len(dfs)==2 and ((dfs[0].columns)[0])=='Subject'):
            table = dfs[0]
            table1=table.dropna()
            return table1
        elif(len(dfs)>=2 and ((dfs[1].columns)[0])=='Subject'):
            table = dfs[1]
            table1=table.dropna()
            return table1
        elif(len(dfs)==1 and ((dfs[0].columns)[0])=='Subject'):
            table = dfs[0]
            table1=table.dropna()
            return table1  
        else:
            print("UNABLE TO DETECT THE TABLE!!!")
    except:
        print("PDF NOT FOUND!!")

con=mysql.connector.connect(
user='username',
password='password',
host='host',
database='db'
)
try:
    if con.is_connected():
        print("connected!")

except Exception as e:
    print("Cannot connect!")
try:
    usn = sys.argv[1] 
    path = sys.argv[2]
    pdf_path=path.replace("\\", "//")

    table = read_table(1)

    table.drop(table.iloc[:,[1,6]],axis=1)

    cur=con.cursor()
            
    # cur.execute("select sum(credits) from subject;")
    # total_credits=cur.fetchall()
    # cur.execute("select count(subject_code) from subject;")
    # subj_count=cur.fetchall()
    # max_marks=int(subj_count[0][0])*100

    cur.execute("select total_credits from total;")
    total_credits=cur.fetchall()
    cur.execute("select max_marks from total;")
    max_marks=cur.fetchall()

    cur.execute("delete from result_db where USN=%s;",(usn,))
    cur.execute("delete from final_result where USN=%s;",(usn,))

    for index,item in table.iterrows():
        val=(usn,item['Subject'],item['Internal'],item['External'],item['Total'],item['Result'])
        sql="insert into result_db(USN,Subject,Internal,External,Total,Result) VALUES (%s,%s,%s,%s,%s,%s);"
        cur.execute(sql,val)
        con.commit() 
        
    cur.execute("update result_db set grades=IF(Total>=90,10,IF(Total>=80,9,IF(Total>=70,8,IF(Total>=60,7,IF(Total>=50,6,IF(Total>=45,5,IF(Total>=40,4,0))))))) where USN=%s;",(usn,))
    cur.execute("UPDATE result_db INNER JOIN subject ON Subject = subject_code SET result_db.credits=subject.credits;")
    cur.execute("update result_db set c_g = grades*credits;")
    cur.execute("insert into final_result(USN) values(%s);",(usn,))
    cur.execute("update final_result set total_marks=(select sum(Total) from result_db where final_result.USN=result_db.USN);")
    cur.execute("update final_result set total_c_g=(select sum(c_g) from result_db where final_result.USN=result_db.USN);")
    cur.execute("update final_result set sgpa=(total_c_g/(%s));",(total_credits[0][0],))
    cur.execute("update final_result set percentage=round((total_marks/%s)*100,2);",(max_marks[0][0],))
    cur.execute("UPDATE final_result set result=if((select count(Result) from result_db where result_db.USN=final_result.USN AND Result='F')>0,'F','P' );")
    cur.execute("update final_result set total_c=(%s);",(total_credits[0][0],))
    con.commit() 
    
    cur.close()
    con.close()

    print("DataBase updated successfully.")

except Exception as e:
    print("DATABASE  UPDATE: ERROR!!! ",e)
