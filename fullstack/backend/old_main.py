# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from zipfile import ZipFile
# from pathlib import Path
# import shutil
# import os
# import uuid
# import base64
# import asyncpg
# import numpy as np
# import cv2
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image as tf_image
# from tensorflow.keras.applications.resnet import ResNet50, preprocess_input
# import json
# from datetime import datetime
# from inference_sdk import InferenceHTTPClient
#
# Rare_Animals_List = ['Irbis']
#
# #-------ФУНКЦИИ ДЛЯ БАЗЫ ДАННЫХ-------#
#
# async def select_output_passports(conn):
#     product = await conn.fetch(f"SELECT * FROM output_passports WHERE output_id = $1", 1)
#     return product
# async def select_zips(conn):
#     product1 = await conn.fetch(f"SELECT * FROM zips")
#     return product1
# async def select_passports(conn):
#     product2 = await conn.fetch(f"SELECT * FROM passports")
#     return product2
# async def select_passports_embadding(conn):
#     passports = await conn.fetch(f"SELECT * FROM passports")
#     pass_embd_list = []
#     for passport in passports:
#         pass_embd_list.append([passport['id'], json.loads(passport['embanding'])])
#     return pass_embd_list
# async def select_passport(conn, passport_id):
#     passport = await conn.fetch(f"SELECT * FROM passports WHERE id = $1", int(passport_id))
#     return passport
# async def select_outputs(conn):
#     product3 = await conn.fetch(f"SELECT * FROM outputs")
#     return product3
# async def select_output(conn, zip_id):
#     output = await conn.fetch(f"SELECT * FROM outputs WHERE zip_id = $1", int(zip_id))
#     return output
# async def select_cords(conn):
#     product4 = await conn.fetch(f"SELECT * FROM cords")
#     return product4
# async def select_cords_by_passport(conn, pass_id):
#     cords = await conn.fetch(f"SELECT * FROM cords WHERE (passport_id = $1)", int(pass_id))
#     return cords
# async def insert_zip(conn, upload_date_str, rare_animals_count, coordinates):
#     upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#     query = 'INSERT INTO Zips (upload_date, rare_animals_count, coordinates) VALUES ($1, $2, $3) RETURNING id;'
#     zip_id = await conn.fetchval(query, upload_date, rare_animals_count, coordinates)
#     return zip_id
# async def insert_output(conn, zip_id, species, count, img_name, confidence, size, pass_id):
#      query = 'INSERT INTO Outputs (zip_id, species, count, processed_photo, confidence, size, pass_id) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;'
#      output_id = await conn.fetchval(query, zip_id, species, count, img_name, float(confidence), float(size), pass_id)
#      return output_id
# async def insert_passport(conn, image_preview, age, gender, cords_id, name):
#     image_path = os.path.join("passports", image_preview)
#     model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top=False,
#                      pooling='avg')
#     result = client.run_workflow(
#         workspace_name="pe1men24",
#         workflow_id="detect-count-and-visualize-2",
#         images={
#             "image": str(image_path)
#         },
#         use_cache=True
#     )
#     def extract_features(img_path):
#         img = tf_image.load_img(img_path, target_size=(224, 224))
#         img_array = tf_image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = preprocess_input(img_array)
#         features = model.predict(img_array)
#         return list(features.flatten())
#     base64_image_string = result[0]['output_image']
#     image_data = base64.b64decode(base64_image_string)
#     for image_cnt in range(int(result[0]['count_objects'])):
#         if result[0]['predictions']['predictions'][image_cnt]['class'] in Rare_Animals_List:
#             img = cv2.imread(image_path)
#             y2 = int(result[0]['predictions']['predictions'][image_cnt]['height'])
#             x2 = int(result[0]['predictions']['predictions'][image_cnt]['width'])
#             y1 = int(result[0]['predictions']['predictions'][image_cnt]['y']) - int(y2 / 2)
#             x1 = int(result[0]['predictions']['predictions'][image_cnt]['x']) - int(x2 / 2)
#             cropped_img = img[y1:y2, x1:x2]
#             path_to_save = 'cropped_passports/' + str(image_cnt) + "_" + str(image_preview)
#             with open(path_to_save, 'wb') as image_file:
#                 image_file.write(image_data)
#             cv2.imwrite(path_to_save, cropped_img)
#             query = 'INSERT INTO Passports (image_preview, type, age, gender, cords_id, embanding, name) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;'
#             embanding = extract_features(path_to_save)
#             passport_id = await conn.fetchval(query, path_to_save, str(result[0]['predictions']['predictions'][image_cnt]['class']), int(age), gender, int(cords_id), str(embanding), str(name))
#             return passport_id
#     return 'Error'
# async def insert_output_passport(conn, output_id, passport_id):
#     query = 'INSERT INTO Output_Passports (output_id, passport_id) VALUES ($1, $2);'
#     return await conn.execute(query, output_id, passport_id)
# async def insert_cords(conn, pass_id, date, coordinates):
#     query = 'INSERT INTO cords (passport_id, date, coordinates) VALUES ($1, $2, $3) RETURNING id'
#     if pass_id is not None:
#         new_cord = await conn.fetchval(query, pass_id, date, str(coordinates))
#     else:
#         new_cord = await conn.fetchval(query, pass_id, date, str(coordinates))
#     return new_cord
# async def update_cords_in_passport(conn, pass_id, cords_id):
#     query = 'UPDATE passports SET cords_id = $2 WHERE id = $1'
#     return await conn.fetchval(query, pass_id, cords_id)
#
#
# async def get_passport_id(passport_embadings_ids: list[list[int, list[float]]], img_path):
#     model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top=False,
#                      pooling='avg')
#     img_path = "uploads/"+img_path
#     def extract_features(img_path):
#         img = tf_image.load_img(img_path, target_size=(224, 224))
#         img_array = tf_image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array = preprocess_input(img_array)
#         features = model.predict(img_array)
#         return list(features.flatten())
#
#     def cosine_similarity(a, b):
#         dot_product = np.dot(a, b)
#         norm_a = np.linalg.norm(a)
#         norm_b = np.linalg.norm(b)
#         return dot_product / (norm_a * norm_b)
#
#     def find_min_sim(top_ids):
#         min_sim = 100
#         min_sim_id = 0
#         for i in range(len(top_ids)):
#             if top_ids[i][1] < min_sim:
#                 min_sim_id = i
#                 min_sim = top_ids[i][1]
#         return min_sim_id
#
#     embading = extract_features(img_path)
#     top_ids = list()
#
#     for passport_id, embading_pass in passport_embadings_ids:
#         if len(top_ids) < 3:
#             cos_sim = cosine_similarity(embading, embading_pass)
#             top_ids.append((passport_id, cos_sim))
#         else:
#             cos_sim = cosine_similarity(embading, embading_pass)
#             min_sim_id = find_min_sim(top_ids)
#             if cos_sim > top_ids[min_sim_id][1]:
#                 top_ids.append((passport_id, cos_sim))
#                 top_ids.pop(min_sim_id)
#     top_ids = sorted(top_ids, key=lambda x: x[1], reverse=True)
#     return top_ids
#
# #---------------------------------- КОД ПОЛУЧЕНИЯ ФАЙЛОВ + ОБРАБОТКА ------------------------------------------#
#
# client = InferenceHTTPClient(
#     api_url="https://detect.roboflow.com",
#     api_key="GyLAEnCOCynKOHoO2JDF"
# )
#
# Date_of_Photos = datetime.today().strftime('%Y-%m-%d')
#
# Date_of_Photo_dict = dict()
#
# async def ReadingAZIPFile(file):
#     zip_results = []
#     zip_path = Path("uploads") / file.filename
#     with open(zip_path, "wb") as buffer:
#         buffer.write(await file.read())
#     with ZipFile(zip_path, "r") as input_zip:
#         for image_path in input_zip.namelist():
#             file_format = image_path.split(".")[-1]
#             if file_format in ["png", "jpg", "jpeg"]:
#                 uploads = os.listdir("uploads")
#                 input_zip.extract(image_path, "uploads")
#                 starter_file_name = image_path
#                 while image_path in uploads:
#                     name = (str(uuid.uuid4())[:10] + "-IriS-" + starter_file_name)
#                     old_file_path = os.path.join("uploads", image_path)
#                     image_path = name
#                     new_file_path = os.path.join("uploads", name)
#                     os.rename(old_file_path, new_file_path)
#                 Date_of_Photo_dict[image_path] = Date_of_Photos
#                 zip_results.append(image_path)
#     return zip_results
#
# IMAGE_DIR = "savedPredictions"
#
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# @app.get("/image/{image_name}")
# async def image(image_name):
#     image_path = os.path.join(IMAGE_DIR, image_name)
#     return FileResponse(image_path)
#
# @app.get("/get_uploads/{zip_id}")
# async def get_uploads(zip_id):
#     to_return = dict()
#     pred = []
#     Animals_Count = dict()
#     conn = await asyncpg.connect(user='postgres',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='81.200.147.154',
#                                  port=5432)
#     animals = await select_output(conn, zip_id)
#     cnt = 0
#     for animal in animals:
#         pred.append(dict())
#         pred[cnt]["IMG"] = animal['processed_photo']
#         pred[cnt]["type"] = animal['species']
#         pred[cnt]["date"] = Date_of_Photos
#         pred[cnt]["size"] = str(animal['size'])
#         pred[cnt]["confidence"] = str(animal['confidence'])
#         pred[cnt]["passport"] = animal['pass_id']
#         if not animal['species'] in Animals_Count.keys():
#             Animals_Count[animal['species']] = 0
#         Animals_Count[animal['species']] += 1
#         cnt += 1
#     to_return['pred'] = pred
#     to_return['diagram'] = Animals_Count
#     return to_return
#
# @app.get("/all_uploads")
# async def all_uploads():
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#     return await select_outputs(conn)
#
# @app.get("/get_passport/{passport_id}")
# async def get_passport(passport_id):
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#     return await select_passport(conn, passport_id)
#
# @app.get("/all_passports")
# async def all_passports():
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#     return await select_passports(conn)
#
# @app.get("/all_zips")
# async def all_zips():
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#     return await select_zips(conn)
#
# @app.get("/pass_preview")
# async def pass_preview(image_name):
#     return FileResponse(image_name)
#
# @app.post("/upload_passport/")
# async def upload_passport(age, gender, cords_sd, cords_vd, name, image_preview: UploadFile = File(...)):
#     coordinates = str(cords_sd)+", "+str(cords_vd)
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#     if image_preview.content_type in ["image/jpeg", "image/png", "image/jpg"]:
#         os.makedirs("passports", exist_ok=True)
#         starter_file_name = image_preview.filename
#         while image_preview.filename in os.listdir("passports"):
#             image_preview.filename = (str(uuid.uuid4())[:10] + "-IriS-" + starter_file_name)
#         image_path = os.path.join("passports", image_preview.filename)
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(image_preview.file, buffer)
#         cords_id = await insert_cords(conn, None, Date_of_Photos, coordinates)
#         return await insert_passport(conn, image_preview.filename, age, gender, cords_id, name)
#     return 'Error'
#
# @app.post("/upload/")
# async def upload_files(cords_sd, cords_vd, files: list[UploadFile] = File(...)):
#     cords = str(cords_sd)+", "+str(cords_vd)
#     os.makedirs("uploads", exist_ok=True)
#     file_list = []
#     for file in files:
#         if file.content_type == ("application/x-zip-compressed" or "application/zip"):
#             for item in (await ReadingAZIPFile(file)):
#                 file_list.append(item)
#
#         elif file.content_type in ["image/jpeg", "image/png", "image/jpg"]:
#
#
#
#             starter_file_name = file.filename
#             while file.filename in os.listdir("uploads"):
#                 file.filename = (str(uuid.uuid4())[:10] + "-IriS-" + starter_file_name)
#             image_path = os.path.join("uploads", file.filename)
#             file_list.append(file.filename)
#             with open(image_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
#             Date_of_Photo_dict[str(file.filename)] = Date_of_Photos
#         else:
#             raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}")
#
#     # ============================-------ОБРАБОТКА ИЗОБРАЖЕНИЙ ИЗ ПАПКИ uploads-------=======================================
#
#
#     Rare_Animals_Count = 0
#
#     Animals_Count = dict()
#
#     Predictions_to_Return = dict()
#
#     pred = []
#
#     for _ in file_list:
#         if str(_).split(".")[-1] in ["jpg", "png", "jpeg"]:
#             image_path = "uploads/" + str(_)
#             result = client.run_workflow(
#                 workspace_name="pe1men24",
#                 workflow_id="detect-count-and-visualize-2",
#                 images={
#                     "image": image_path
#                 },
#                 use_cache=True
#             )
#
#             # ---СОХРАНЕНИЕ ОБРАБОТАННОГО ИЗОБРАЖЕНИЯ В ПАПКУ---
#             base64_image_string = result[0]['output_image']
#             image_data = base64.b64decode(base64_image_string)
#             path_to_save = "savedPredictions/" + str(_)
#             with open(path_to_save, 'wb') as image_file:
#                 image_file.write(image_data)
#
#             for image_cnt in range(int(result[0]['count_objects'])):
#                 predict_dict = dict()
#                 predict_dict['IMG'] = str(_)
#                 predict_dict['type'] = str(result[0]['predictions']['predictions'][image_cnt]['class'])
#                 predict_dict['date'] = Date_of_Photo_dict[str(_)]
#                 predict_dict['size'] = str(result[0]['predictions']['predictions'][image_cnt]['width'])
#                 predict_dict['confidence'] = str(result[0]['predictions']['predictions'][image_cnt]['confidence'])
#                 predict_dict['passport'] = None
#
#                 pred.append(predict_dict)
#
#                 if predict_dict['type'] in Rare_Animals_List:
#                     Rare_Animals_Count += 1
#                     img = cv2.imread(image_path)
#                     y2 = int(result[0]['predictions']['predictions'][image_cnt]['height'])
#                     x2 = int(result[0]['predictions']['predictions'][image_cnt]['width'])
#                     y1 = int(result[0]['predictions']['predictions'][image_cnt]['y']) - int(y2 / 2)
#                     x1 = int(result[0]['predictions']['predictions'][image_cnt]['x']) - int(x2 / 2)
#                     cropped_img = img[y1:y2, x1:x2]
#                     path_to_save = 'cropped_images/' + str(image_cnt) + "_" + str(_)
#                     with open(path_to_save, 'wb') as image_file:
#                         image_file.write(image_data)
#                     cv2.imwrite(path_to_save, cropped_img)
#                 if not predict_dict['type'] in Animals_Count.keys():
#                     Animals_Count[predict_dict['type']] = 0
#                 Animals_Count[predict_dict['type']] += 1
#
#     Predictions_to_Return['pred'] = pred
#     Predictions_to_Return['diagram'] = Animals_Count
#
#
#     #----------------------- ОТПРАВКА ДАННЫХ НА БАЗУ ДАННЫХ -------------------------#
#     conn = await asyncpg.connect(user='sirius',
#                                  password='Sirius228',
#                                  database='sirius',
#                                  host='92.255.107.199',
#                                  port=5432)
#
#
#     try:
#         cords_id = 'null'
#         if Predictions_to_Return['pred'] != []:
#             for file in Predictions_to_Return['pred']:
#                 passport_id = None
#                 if file['type'] in Rare_Animals_List:
#                     pass_embd = await select_passports_embadding(conn)
#                     possible_passport_id = await get_passport_id(pass_embd, file['IMG'])
#                     passport_id = int(possible_passport_id[0][0])
#                     cords_id = await insert_cords(conn, passport_id, Date_of_Photos, cords)
#                     await update_cords_in_passport(conn, passport_id, cords_id)
#                 else:
#                     cords_id = await insert_cords(conn, passport_id, Date_of_Photos, cords)
#
#             zip_id = await insert_zip(conn, Date_of_Photos, Rare_Animals_Count, cords)
#             for file in Predictions_to_Return['pred']:
#                 if file['type'] in Rare_Animals_List:
#                     pass_embd = await select_passports_embadding(conn)
#                     possible_passport_id = await get_passport_id(pass_embd, file['IMG'])
#                     file['passport'] = int(possible_passport_id[0][0])
#                     output_id = await insert_output(conn, zip_id, file['type'], 1, file['IMG'], file['confidence'], file['size'], file['passport'])
#                     await insert_output_passport(conn, output_id, int(possible_passport_id[0][0]))
#                 else:
#                     await insert_output(conn, zip_id, file['type'], 1, file['IMG'], file['confidence'], file['size'], file['passport'])
#
#     finally:
#         await conn.close()
#     return Predictions_to_Return