import streamlit as st
import pyodbc
#import secret
import pandas as pd
import datetime
import toml


# Create a connection string
def init_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};SERVER="
        + st.secrets["Server"]
        + ";DATABASE="
        + st.secrets["Database"]
        + ";UID="
        + st.secrets["Username"]
        + ";PWD="
        + st.secrets["Password"]
    )
#Calling the function
conn = init_connection()
#Creating a cursor
mycursor = conn.cursor()

#Create App : 
def main():
    st.title("MBNL Work Order Management");
    #Display Options for CRUD operations
    st.sidebar.warning("Please Select the WO Type:")
    typeofwo = st.sidebar.radio("WO Types Available:", ["LOS","BTFEAS"])
    if typeofwo == "LOS":
        option = st.radio("Select an Operation", ["Create","View"])
        #Perform Selected CRUD Operation
        if option == "Create":
            st.subheader("Create a Record") 
            # Get the list of Dropdowns for fields =  projects, catagory, and planners from the database 
            mycursor.execute("SELECT [Display] FROM [ref].[Project_Name_coordination]")
            project_list = mycursor.fetchall()
            mycursor.execute("SELECT [Display] FROM [ref].[LOS_Category]")
            LOSTask_list = mycursor.fetchall()
            mycursor.execute("SELECT [Display] FROM [ref].[Planner]")
            planner_list = mycursor.fetchall()

            cella = st.text_input("AEnd TMCell*")
            cellb = st.text_input("BEnd TMCell*")
            #project = st.text_input("Project")
            project_dropdown = st.selectbox("Project*", options=[item[0] for item in project_list], key="project_dropdown",index=None)
            project = project_dropdown
            comment = st.text_input("Comment")
            #planner = st.text_input("Planner")
            planner_dropdown = st.selectbox("Planner*", options=[item[0] for item in planner_list], key="planner_dropdown",index=None)
            planner = planner_dropdown
            task_dropdown = st.selectbox("LOS Catagory*", options=[item[0] for item in LOSTask_list], key="task_dropdown",index=None)
            LOStask = task_dropdown
            #task = st.text_input("Task")
            disha = st.number_input("AEnd Dish Height*",value=None)
            dishb = st.number_input("BEnd Dish Height*",value=None)
            bearinga = st.number_input("AEnd Bearing*",value=None)
            bearingb = st.number_input("BEnd Bearing*",value=None)
            ordertype_dropdown = st.selectbox("Order Type*", options=["LOS","BTFEAS"], key="ordertype_dropdown",index=0)
            ordertype = ordertype_dropdown
            date = st.date_input("Date Created",datetime.date.today())


            if st.button("Create"):
                if cella == "" or cellb == "" or project == "" or planner == "" or disha == "" or dishb == "" or bearinga == "" or bearingb == "" or ordertype == "":
                    st.error("Please Fill in Mandatory Fields the details before creating record")
                else:

                    #project = project_dropdown
                    #task = task_dropdown
                    #planner = planner_dropdown
                    sql = "INSERT INTO i.WO_Management([A_End_TMCell_ID],[B_End_TMCell_ID],[Project],[Comments],[Planner_Requested],[LOS_Catagory],[A_End_Dish_Height],[B_End_Dish_Height],[A_End_Bearing],[B_End_Bearing],[Order_Type],[Created_On]) values (?,?,?,?,?,?,?,?,?,?,?,?)"
                    val = (cella,cellb,project,comment,planner,LOStask,disha,dishb,bearinga,bearingb,ordertype,date)
                    mycursor.execute(sql,val)
                    conn.commit()
                    st.success("Record Created Successfully!!!")
                    mycursor.execute("select top 1 WO_Number from [i].[WO_Management]  order by [WO_Number] desc")
                    results = mycursor.fetchall()
                    st.markdown("# Work Order Number")
                    st.write("# **{}**".format(results[0][0]))
                    st.balloons()
                    
        elif option == "View":
            st.subheader("Read Records")
            df = pd.read_sql("SELECT [WO_Number],[A_End_TMCell_ID],[B_End_TMCell_ID],[Project],[Planner_Requested],[LOS_Catagory],[A_End_Dish_Height],[B_End_Dish_Height],[A_End_Bearing],[B_End_Bearing],[Order_Type],[Created_On] from [i].[WO_Management] where Order_Type = 'LOS'", conn)
            st.dataframe(df)
    
    elif typeofwo == "BTFEAS":
        option = st.radio("Select an Operation", ["Create","View"])
        #Perform Selected CRUD Operation
        if option == "Create":
            st.subheader("Create a Record") 
            # Get the list of Dropdowns for fields =  projects, bT Tasks, and planners from the database 
            mycursor.execute("SELECT [Display] FROM [ref].[Project_Name_coordination]")
            project_list = mycursor.fetchall()
            mycursor.execute("SELECT [Display] FROM [ref].[Planner]")
            planner_list = mycursor.fetchall()
            mycursor.execute("SELECT [Display] FROM [ref].[BT_Feasibility_Task]")
            BTFEAS_list = mycursor.fetchall()

            cella = st.text_input("AEnd TMCell*")
            #project = st.text_input("Project")
            project_dropdown = st.selectbox("Project*", options=[item[0] for item in project_list], key="project_dropdown",index=None)
            project = project_dropdown
            comment = st.text_input("Comment")
            #planner = st.text_input("Planner")
            planner_dropdown = st.selectbox("Planner*", options=[item[0] for item in planner_list], key="planner_dropdown",index=None)
            planner = planner_dropdown
            task_dropdown = st.selectbox("BTFEAS Task*", options=[item[0] for item in BTFEAS_list], key="task_dropdown",index=None)
            BTFEAStask = task_dropdown
            #task = st.text_input("Task")
            ordertype_dropdown = st.selectbox("Order Type*", options=["LOS","BTFEAS"], key="ordertype_dropdown",index=1)
            ordertype = ordertype_dropdown
            date = st.date_input("Date Created",datetime.date.today())


            if st.button("Create"):
                if cella == "" or project == "" or planner == "" or ordertype == "" or BTFEAStask == "":
                    st.error("Please Fill in Mandatory Fields before creating record")
                else:

                    #project = project_dropdown
                    #task = task_dropdown
                    #planner = planner_dropdown
                    sql = "INSERT INTO i.WO_Management([A_End_TMCell_ID],[Project],[Comments],[Planner_Requested],[BTFEAS_Task],[Order_Type],[Created_On]) values (?,?,?,?,?,?,?)"
                    val = (cella,project,comment,planner,BTFEAStask,ordertype,date)
                    mycursor.execute(sql,val)
                    conn.commit()
                    st.success("Record Created Successfully!!!")
                    mycursor.execute("select top 1 WO_Number from [i].[WO_Management]  order by [WO_Number] desc")
                    results = mycursor.fetchall()
                    st.markdown("# Work Order Number")
                    st.write("# **{}**".format(results[0][0]))
                    st.balloons()
                    
        elif option == "View":
            st.subheader("Read Records")
            df = pd.read_sql("SELECT [WO_Number],[A_End_TMCell_ID],[Project],[Planner_Requested],[BTFEAS_Task],[Order_Type],[Created_On] from [i].[WO_Management] where Order_Type = 'BTFEAS'", conn)
            st.dataframe(df)


if __name__ == "__main__":
    main()




