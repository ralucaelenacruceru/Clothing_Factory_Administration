from flask import Flask, render_template, flash, g
from flask import redirect, url_for, request
import psycopg2
from psycopg2 import errors
import traceback

app = Flask(__name__)
app.secret_key = 'raluca_are_cheie_secreta'


# Function to establish a database connection
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(database="ClothesFactory", user="postgres", password="raluca", host="localhost",
                                port="5432")
    return g.db


# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcomepage.html')


# Route for displaying factory information
@app.route('/infocolabfactory', methods=['GET', 'POST'])
def info_factory():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM "Factory" ''')
    data = cur.fetchall()

    cur.close()

    return render_template('infocolabfactory.html', data=data)


# Route for managing factories
@app.route('/managecolabfactory', methods=['GET', 'POST'])
def manage_factory():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM "Factory" ''')
    data = cur.fetchall()

    cur.close()

    return render_template('managecolabfactory.html', data=data)


# Route for displaying the create factory page
@app.route('/createFacPage')
def create_fac_page():
    return render_template('createfactory.html')


# Route for creating a new factory
@app.route('/createfactory', methods=['POST'])
def create_factory():
    conn = get_db()
    cur = conn.cursor()

    name_factory = request.form['NameFactory']
    contact_name = request.form['ContactName']
    city = request.form['City']
    country = request.form['Country']
    address = request.form['Address']
    postal_code = request.form['PostalCode']

    try:
        cur.execute(
            '''INSERT INTO public."Factory" ("NameFactory", "ContactName", "City", "Country", "Address", "PostalCode") 
               VALUES (%s, %s, %s ,%s, %s, %s)''',
            (name_factory, contact_name, city, country, address, postal_code))
        conn.commit()
        flash('Factory added successfully!', 'success')

    except errors.UniqueViolation as ve:
        flash(f'Error: {ve}', 'error')

    except ValueError as ve:
        flash(f'Invalid Format! {ve}', 'error')

    except Exception as e:
        traceback.print_exc()
        conn.rollback()
        flash('An error occurred during database operation!', 'error')

    finally:
        cur.close()

    return redirect(url_for('manage_factory'))


# Route for deleting a factory
@app.route('/deletefactory', methods=['GET', 'POST'])
def delete_factory():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        factory_id = request.form.get('factory_id')
    else:
        factory_id = request.args.get('factory_id')

    try:

        if factory_id and factory_id.strip():

            factory_id = int(factory_id)
            cur.execute('''DELETE FROM "Factory" WHERE "factory_id" = %s''', (factory_id,))
            conn.commit()
            flash('Factory deleted successfully!', 'success')
        else:
            flash('Invalid factory ID!', 'error')

    except ValueError as ve:
        flash(f'Invalid Format! {ve}', 'error')

    except Exception as e:
        traceback.print_exc()
        flash(f'Error: {e}', 'error')

    finally:

        cur.close()

    return redirect(url_for('manage_factory'))


# Route for updating a factory
@app.route('/updatefactory/<int:factory_id>', methods=['GET'])
def update_factory(factory_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM public."Factory" WHERE "factory_id" = %s''', (factory_id,))
    factory_data = cur.fetchone()

    cur.close()

    return render_template('updatecolabfactory.html', factory_data=factory_data)


# Route for performing the update of a factory
@app.route('/updatefactory/<int:factory_id>', methods=['POST'])
def perform_update_factory(factory_id):
    conn = get_db()
    cur = conn.cursor()

    name_factory = request.form['NameFactory']
    contact_name = request.form['ContactName']
    city = request.form['City']
    country = request.form['Country']
    address = request.form['Address']
    postal_code = request.form['PostalCode']

    try:
        cur.execute(
            '''UPDATE public."Factory" 
            SET "NameFactory"=%s, "ContactName"=%s, "City"=%s, "Country"=%s, "Address"=%s, "PostalCode"=%s 
            WHERE "factory_id"=%s''',
            (name_factory, contact_name, city, country, address, postal_code, factory_id))
        conn.commit()
        flash('Factory updated successfully!', 'success')
    except ValueError as ve:
        flash(f'Invalid Format! {ve}', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')

    finally:
        cur.close()

    return redirect(url_for('manage_factory'))


# Route for displaying product type information
@app.route('/infoprodtype', methods=['GET', 'POST'])
def info_prod_type():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT "CategoryName" FROM "Category"''')

    categories = cur.fetchall()
    categorii = [row[0] for row in categories]

    cur.execute('''SELECT "NameProductType", "ProductPrice", "Color", "Quantity", "IsDiscontinued", PT."ProductType_ID"
                        FROM "ProductType" AS PT
                        JOIN "Factory2ProductType" AS FP ON PT."ProductType_ID" = FP."ProductType_ID"
                        WHERE FP."factory_id" = %s''', (2,))

    category_data = cur.fetchall()
    cur.close()

    return render_template('infoprodtype.html', category_data=category_data, categories=categorii)


# Route for displaying product type information for management
@app.route('/infoprodtype2', methods=['GET', 'POST'])
def info_prod_type2():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT "CategoryName" FROM "Category"''')

    categories = cur.fetchall()
    categories2 = [row[0] for row in categories]

    cur.execute('''SELECT "NameProductType", "ProductPrice", "Color", "Quantity", "IsDiscontinued", PT."ProductType_ID"
                        FROM "ProductType" AS PT
                        JOIN "Factory2ProductType" AS FP ON PT."ProductType_ID" = FP."ProductType_ID"
                        WHERE FP."factory_id" = %s''', (2,))

    category_data = cur.fetchall()
    cur.close()

    return render_template('manageprodtype.html', category_data=category_data, categories=categories2)


# Route for creating a new product type
@app.route('/createprodtype', methods=['GET', 'POST'])
def create_prod_type():
    conn = get_db()
    cur = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()

    cur3.execute('''SELECT "CategoryName" FROM "Category"''')

    categories = cur3.fetchall()
    # categorii = [row[0] for row in categories]


    cur3.execute('''SELECT "NameMaterial" FROM "Material''')
    materials = cur3.fetchall()

    if request.method == 'POST':

        category_name = request.form['CategoryName']
        price = request.form['Price']
        color = request.form['Color']
        qty = request.form['Quantity']
        is_disc = request.form.get('isDiscontinued', 'false')
        name_product_type = request.form['NameProductType']

        # Retrieve category ID based on category name
        cur.execute('''SELECT "Category_ID" FROM "Category" C WHERE C."CategoryName" = %s ''', (category_name,))
        category_id = cur.fetchone()


        try:
            # Insert new product type into the database
            cur.execute(
                '''INSERT INTO public."ProductType" 
                ("Categorie_ID", "ProductPrice", "Color", "Quantity", "IsDiscontinued", "NameProductType")
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING "ProductType_ID" ''',
                (category_id, price, color, qty, is_disc, name_product_type))

            product_type_id = cur.fetchone()[0]

            # Associate the new product type with the factory
            cur2.execute('''INSERT INTO public."Factory2ProductType" ("factory_id", "ProductType_ID") VALUES(%s, %s)''',
                         (2, product_type_id))
            conn.commit()
            flash('Factory added successfully!', 'success')

        except errors.UniqueViolation as ve:
            print("UniqueViolation Error:", ve)
            flash(f'Error: {ve}', 'error')

        except ValueError as ve:
            print("ValueError:", ve)
            flash(f'Invalid Format! {ve}', 'error')

        except Exception as e:
            print("Generic Error:", e)
            traceback.print_exc()
            conn.rollback()  # Rollback the transaction
            flash('An error occurred during database operation!', 'error')

        finally:
            cur.close()
            cur2.close()
            cur3.close()

        # Redirect to the info_prod_type2 route with query parameters
        return redirect(url_for('info_prod_type2', categories=categories))

    # If the request method is GET, render the create product type form
    return render_template('createprodtype.html', categories=categories, materials=materials)


# Route for deleting a product type
@app.route('/deleteprodtype', methods=['GET', 'POST'])
def delete_prod_type():
    conn = get_db()
    cur = conn.cursor()
    cur2 = conn.cursor()

    if request.method == 'POST':
        # If it's a POST request, get the productType_ID from the form data
        product_type_id = request.form.get('productType_ID')
    else:
        # If it's a GET request, get the productType_ID from the URL parameters
        product_type_id = request.args.get('productType_ID')

    try:

        if product_type_id and product_type_id.strip():

            product_type_id = int(product_type_id)
            # Delete the product type from the ProductType table
            cur.execute('''DELETE FROM "ProductType" WHERE "ProductType_ID" = %s''', (product_type_id,))

            # Delete the product type from the Factory2ProductType table
            cur2.execute('''DELETE FROM "Factory2ProductType" WHERE "ProductType_ID" = %s''', (product_type_id,))

            conn.commit()
            flash('Product Type deleted successfully!', 'success')
        else:
            flash('Invalid Product Type ID!', 'error')

    except ValueError as ve:
        flash(f'Invalid Format! {ve}', 'error')

    except Exception as e:
        traceback.print_exc()
        flash(f'Error: {e}', 'error')
    finally:

        cur.close()
    return redirect(url_for('info_prod_type2'))


# Route for updating a product type
@app.route('/updateprodtype/<int:productType_id>', methods=['GET'])
def update_category(productType_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM public."ProductType" WHERE "ProductType_ID" = %s''', (productType_id,))
    product_data = cur.fetchone()
    cur.close()

    return render_template('updateprodtype.html', product_data=product_data)


# Route for performing the update of a product type
@app.route('/updateprodtype/<int:productType_id>', methods=['POST'])
def perform_update_prod_type(productType_id):
    conn = get_db()
    cur = conn.cursor()

    product_price = request.form['ProductPrice']
    quantity = request.form['Quantity']
    is_discontinued = request.form.get('isDiscontinued', 'false')

    try:
        # Update product type information in the ProductType table
        cur.execute(
            '''UPDATE public."ProductType" 
            SET "ProductPrice"=%s, "Quantity"=%s, "IsDiscontinued"=%s WHERE "ProductType_ID"=%s''',
            (product_price, quantity, is_discontinued, productType_id))
        conn.commit()
        flash('Product type updated successfully!', 'success')
    except ValueError as ve:
        flash(f'Invalid Format! {ve}', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')

    finally:
        cur.close()

    return redirect(url_for('info_prod_type2'))


# Route for displaying store information
@app.route('/infoStores', methods=['GET', 'POST'])
def info_stores():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT CS."StoreName", CS."City", F2CS."ContractDate"
                            FROM "ColabStores" AS CS
                            JOIN "Factory2ColabStores" AS F2CS ON CS."ColabStores_ID" = F2CS."ColabStores_ID"
                            JOIN "Factory" AS F ON F."factory_id" = F2CS."Factory_ID"
                            WHERE F."factory_id" = %s''', (2,))

    data = cur.fetchall()
    cur.close()

    return render_template('infostores.html', data=data)


# Route for displaying store statistics
@app.route('/storestats', methods=['GET', 'POST'])
def store_stats():
    conn = get_db()
    cur = conn.cursor()
    cur1 = conn.cursor()

    cur1.execute('''SELECT CS."StoreName",
                            (SELECT COUNT(*)
                             FROM "Product" P
                             WHERE P."ColabStores_ID" = F2CS."ColabStores_ID"
                               AND P."DateFabrication" > F2CS."ContractDate") AS NumarProduseFabricate
                        FROM
                            "Factory2ColabStores" F2CS
                        JOIN
                            "ColabStores" CS ON CS."ColabStores_ID" = F2CS."ColabStores_ID"
                        WHERE (
                            SELECT COUNT(*)
                            FROM "Product" P
                            WHERE P."ColabStores_ID" = F2CS."ColabStores_ID"
                              AND P."DateFabrication" > F2CS."ContractDate"
                        ) IS NOT NULL;''', )

    sb4_data = cur1.fetchall()

    cur.close()

    return render_template('statisticsstore.html', sb4_data=sb4_data)


# Route for displaying material information related to a product type
@app.route('/infomaterials/<int:productType_id>', methods=['GET', 'POST'])
def info_materials(productType_id):
    conn = get_db()
    cur = conn.cursor()

    search_query = request.args.get('search', default='', type=str)

    cur.execute('''SELECT M."NameMaterial", M."Material_ID"
                            FROM "Material" AS M
                            JOIN "ProductType2Material" AS PT2M ON M."Material_ID" = PT2M."Material_ID"
                            JOIN "ProductType" AS PT ON PT."ProductType_ID" = PT2M."ProductType_ID"
                            WHERE PT."ProductType_ID" = %s AND M."UnityPrice" > 100''', (productType_id,))

    data = cur.fetchall()
    print(data)
    cur.close()

    return render_template('infomaterial.html', data=data, search_query=search_query)


# Route for displaying category information related to a product type
@app.route('/infocategory/<int:productType_id>', methods=['GET', 'POST'])
def info_category(productType_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT C."CategoryName"
                            FROM "Category" AS C
                            JOIN "ProductType" AS PT ON PT."Categorie_ID" = C."Category_ID"
                            WHERE PT."ProductType_ID" = %s ''', (productType_id,))

    cat_data = cur.fetchall()
    cur.close()

    return render_template('infocategory.html', cat_data=cat_data)


# Route for displaying defect information related to a product type
@app.route('/infodefects/<int:productType_id>', methods=['GET', 'POST'])
def info_defects(productType_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT COUNT(P."Defect")
                    FROM "Product" AS P
                    JOIN "ProductType" AS PT ON PT."ProductType_ID" = P."ProductType_ID"
                    WHERE PT."ProductType_ID" = %s
                    AND P."Defect" = true
                    GROUP BY PT."ProductType_ID" ''', (productType_id,))

    def_data = cur.fetchall()
    cur.close()

    return render_template('infodefects.html', def_data=def_data)


# Route for displaying supplier information related to a material
@app.route('/infosupplier/<int:material_id>', methods=['GET', 'POST'])
def info_supplier(material_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT S."NameSupplier", S."City", S."Country"
                            FROM "Supplier" AS S
                            JOIN "Material" AS M ON M."Supplier_ID" = S."Supplier_ID"
                            WHERE M."Material_ID" = %s''', (material_id,))

    datasup = cur.fetchall()
    print(datasup)
    cur.close()

    return render_template('infosupplier.html', datasup=datasup)


# Route for displaying product statistics
@app.route('/prodstats2/<int:productType_id>', methods=['GET', 'POST'])
def prod_stats2(productType_id):
    conn = get_db()
    cur = conn.cursor()
    cur1 = conn.cursor()
    cur.execute('''SELECT CS."StoreName", CS."Address"
                    FROM "ColabStores" AS CS
                    JOIN (
                        SELECT "ColabStores_ID"
                        FROM "Product"
                        WHERE "ProductType_ID" = %s
                        GROUP BY "ColabStores_ID"
                        ORDER BY COUNT(*) DESC
                        LIMIT 1
                    ) subquery ON  CS."ColabStores_ID" = subquery."ColabStores_ID";''', (productType_id,))

    cur1.execute('''SELECT S."NameSupplier",
                       (SELECT COUNT(M."Material_ID")
                        FROM "Material" M
                        JOIN "ProductType2Material" T2M ON M."Material_ID" = T2M."Material_ID"
                        JOIN "ProductType" TP ON T2M."ProductType_ID" = TP."ProductType_ID"
                        WHERE TP."ProductType_ID" = %s
                          AND M."Supplier_ID" = S."Supplier_ID"
                       ) AS NumarMateriale
                FROM "Supplier" S
                WHERE (
                        SELECT COUNT(M."Material_ID")
                        FROM "Material" M
                        JOIN "ProductType2Material" T2M ON M."Material_ID" = T2M."Material_ID"
                        JOIN "ProductType" TP ON T2M."ProductType_ID" = TP."ProductType_ID"
                        WHERE TP."ProductType_ID" = '2'
                          AND M."Supplier_ID" = S."Supplier_ID"
                      ) IS NOT NULL
                ORDER BY NumarMateriale DESC
                LIMIT 1;''', (productType_id,))

    sb1_data = cur.fetchall()
    sb2_data = cur1.fetchall()
    cur.close()

    return render_template('statisticsprod2.html', sb1_data=sb1_data, sb2_data=sb2_data)


# Route for displaying product statistics
@app.route('/prodstats', methods=['GET', 'POST'])
def prod_stats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''SELECT PT."ProductType_ID",
    PT."NameProductType",
    PT."ProductPrice",
    (SELECT SUM(M."UnityPrice")
     FROM "Material" M
     JOIN "ProductType2Material" T2M ON M."Material_ID" = T2M."Material_ID"
     WHERE T2M."ProductType_ID" = PT."ProductType_ID") AS CostMateriale,
    (PT."ProductPrice" - (SELECT SUM(M."UnityPrice")
                       FROM "Material" M
                       JOIN "ProductType2Material" T2M ON M."Material_ID" = T2M."Material_ID"
                       WHERE T2M."ProductType_ID" = PT."ProductType_ID" )) AS Profit
    FROM "ProductType" PT
    ORDER BY Profit DESC NULLS LAST; ''')
    sb3_data = cur.fetchall()

    cur.close()

    return render_template('statisticsprod.html', sb3_data=sb3_data)


# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
