import pymysql

# 增删改查操作

def select_db(select_sql):
    """查询"""
    # 建立数据库连接
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="083332aa",
        db="plane"
    )
    # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        # 使用 execute() 执行sql
        cur.execute(select_sql)
        db.commit()
    except:
        db.rollback()
        # 使用 fetchall() 获取所有查询结果
    data = cur.fetchall()
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    db.close()
    return data



def insert_db(insert_sql):
    """查询"""
    # 建立数据库连接
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="083332aa",
        db="plane"
    )
    # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
    cur = db.cursor()
    try:
        # 使用 execute() 执行sql
        cur.execute(insert_sql)
        db.commit()
    except:
        db.rollback()
        cur.close()
        # 关闭数据库连接
        db.close()
        return False
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    db.close()
    return True




def update_db(update_sql):
    """更新"""
    # 建立数据库连接
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="083332aa",
        db="plane"
    )
    # 通过 cursor() 创建游标对象
    cur = db.cursor()
    try:
        # 使用 execute() 执行sql
        cur.execute(update_sql)
        # 提交事务
        db.commit()
    except Exception as e:
        print("操作出现错误：{}".format(e))
        # 回滚所有更改
        db.rollback()
    finally:
        # 关闭游标
        cur.close()
        # 关闭数据库连接
        db.close()



def delete_db(delete_sql):
    """删除"""
    # 建立数据库连接
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="083332aa",
        db="plane"
    )
    # 通过 cursor() 创建游标对象
    cur = db.cursor()
    try:
        # 使用 execute() 执行sql
        cur.execute(delete_sql)
        # 提交事务
        db.commit()
    except Exception as e:
        print("操作出现错误：{}".format(e))
        # 回滚所有更改
        db.rollback()
    finally:
        # 关闭游标
        cur.close()
        # 关闭数据库连接
        db.close()





if __name__ == '__main__':
    # sql ="INSERT INTO t_user(`username`,`password`) VALUES('xu','123456')"
    # ifsuccess = insert_db(sql)
    # if ifsuccess == True:
    #     print("插入成功")

    delete_sql = 'DELETE FROM t_user WHERE id = 5'
    delete_db(delete_sql)