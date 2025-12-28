import pandas as pd
import mysql.connector
try:
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
        
    cur=con.cursor()

    cur.execute('select USN from student;')
    get_student=cur.fetchall()
    cur.execute('select subject_code from subject;')
    get_subject=cur.fetchall()

    lst_student=[]
    lst_subject=[]


    for i in get_student:
        lst_student.append(i[0])
    for j in get_subject:
        lst_subject.append(j[0])
        

    d=pd.DataFrame()

    for j in lst_student:
        df = pd.DataFrame()
        for i in lst_subject:
            cur.execute("select Internal,External,Total,result_db.credits,Grades,c_g,Result from result_db inner join subject ON result_db.Subject=subject.subject_code where USN=%s and Subject=%s;",(j,i,))
            l=cur.fetchall()
            cols = pd.MultiIndex.from_tuples([(i, "IN"),(i, "EX"),(i, "TOT"),(i, "C"),(i,"G"),(i,"C*G"),(i,"RES")],names=['SUBJECT CODE','USN'])
            dfs=pd.DataFrame(l, columns=cols,index=(j,))
            df=pd.concat([df,dfs],axis=1)
        cur.execute("select total_c_g,total_c,sgpa,total_marks,percentage,result from final_result where USN=%s;",(j,))
        ls=cur.fetchall()
        cols1 = pd.MultiIndex.from_tuples([(' ', 'Total C*GP'),(' ','Total C'),(' ', 'SGPA'),(' ', 'Total Marks'),(' ', '%'),(' ','Result')])
        dn=pd.DataFrame(ls, index=(j,), columns=cols1)
        df=pd.concat([df,dn],axis=1)
        d=pd.concat([d,df],axis=0,names=['SUBJECT CODE','USN'])

    cur.execute("select student.USN,student.name,percentage from final_result inner join student on final_result.USN=student.USN order by percentage desc limit 3;")
    toppers=cur.fetchall()
    frame=pd.DataFrame(toppers,columns=['USN','Name','%'])

    with pd.ExcelWriter('result_analysis.xlsx',engine='openpyxl') as writer:   
        d.style.set_properties(**{'text-align': 'center'}).to_excel(writer,index=True,sheet_name='result sheet')
        frame.to_excel(writer,sheet_name='Topper',index=False)

    cur.close()
except Exception as e:
    print("INTERNAL ERROR!!! ",e)