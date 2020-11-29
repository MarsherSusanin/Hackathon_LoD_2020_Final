from catboost import CatBoostRegressor

if __name__ == '__main__':
    clf = CatBoostRegressor()

    test = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
    # больше примеров тут test_data.csv

    for model in ['arterial_hypertension.dump', 'ONMK.dump', 'stenokardiya.dump', 'ssnedost.dump', 'other_heart_disease.dump']:
        clf.load_model(model)
        pred=clf.predict(test, prediction_type='Probability')
        print('Вероятность {}: {:.4f}'.format(model, pred[1]))