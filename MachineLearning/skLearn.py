from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from scipy.misc import imread, imresize
from sklearn import datasets, svm

tl_ratio = 2


def classify(img, classifier):
    img = resize(img)
    return classifier.predict(img.reshape((1, img.shape[0] * img.shape[1])))[0]


def setup_classifier():
    knn = KNeighborsClassifier(3)
    digits = datasets.load_digits()
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    knn.fit(data[:n_samples // 2], digits.target[:n_samples // 2])
    return knn


def resize(img):
    pic = imresize(img, (8, 8))
    pic = pic[:, :, 0]

    for y, val in enumerate(pic):
        for x, val2 in enumerate(val):
            new_value = 16 - round((val2 / 255) * 16)
            pic[y][x] = new_value
    return pic

def get_pic(path):
    pic = imread(path)
    pic = imresize(pic, (8, 8))
    pic = pic[:, :, 0]

    for y, val in enumerate(pic):
        for x, val2 in enumerate(val):
            new_value = 16 - round((val2 / 255) * 16)
            pic[y][x] = new_value
    return pic


def optimize_forest(digits, pic):
    for depth in range(1, 20):
        for n in range(1, 20):
            example = RandomForestClassifier(max_depth=depth, n_estimators=n, max_features=1)
            res = test_classifier(example, digits, pic, False)
            print("random forest with depth=", depth, "and n=", n, "have score of:", res)


def optimize_neuro(digits, pic):
    for x in range(1, 20):
        x /= 10
        example = MLPClassifier(alpha=x)
        res = test_classifier(example, digits, pic, False)
        print("Neuron web with", x, "alpha have score of:", res)


def optimize_tree(digits, pic):
    for x in range(1, 20):
        example = DecisionTreeClassifier(max_depth=x)
        res = test_classifier(example, digits, pic, False)
        print("Decision tree with", x, "depth have score of:", res)


def optimize_knn(digits, pic):
    for x in range(1, 10):
        example = KNeighborsClassifier(x)
        res = test_classifier(example, digits, pic, False)
        print("Knn with", x, "neighbours have score of:", res)


def optimize_svm(digits, pic):
    for gamma in range(1, 20):
        gamma /= 20
        for c in range(1, 20):
            c /= 20
            example = svm.SVC(gamma=gamma, C=c)
            res = test_classifier(example, digits, pic, False)
            print("SVM with gamma=", gamma, "and C=", c, "have score of:", res)


def test_classifier(classifier, digits, pic, trace=True):
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    classifier.fit(data[:n_samples // tl_ratio], digits.target[:n_samples // tl_ratio])
    result = classifier.score(data[n_samples // tl_ratio:], digits.target[n_samples // tl_ratio:])
    pic_result = classifier.predict(pic.reshape((1, pic.shape[0] * pic.shape[1])))[0]
    if trace:
        print(str(classifier).split("(")[0], "predicted:", pic_result, "(", result, ")")
    return result


def show_output():
    digits = datasets.load_digits()
    for x in range(1, 10):
        print(x, "-----------------------------------", x)
        file = str(x) + ".jpg"
        pic = get_pic(file)
        svm_class = svm.SVC(gamma=2, C=1)
        knn = KNeighborsClassifier(3)
        tree_class = DecisionTreeClassifier(max_depth=7)
        neur_class = MLPClassifier(alpha=1.5)
        rfor_class = RandomForestClassifier(max_depth=7, n_estimators=15, max_features=1)
        test_classifier(svm_class, digits, pic)
        test_classifier(knn, digits, pic)
        test_classifier(tree_class, digits, pic)
        test_classifier(neur_class, digits, pic)
        test_classifier(rfor_class, digits, pic)
        print("-------------------------------------")


digits = datasets.load_digits()
pic = get_pic("1.jpg")

import warnings
warnings.filterwarnings("ignore")
# test_classifier(svm_class, digits, pic)
# test_classifier(knn, digits, pic)
# test_classifier(tree_class, digits, pic)
# test_classifier(neur_class, digits, pic)
# test_classifier(rfor_class, digits, pic)

#optimize_knn(digits, pic)
#optimize_svm(digits, pic)
#optimize_tree(digits, pic)
#optimize_neuro(digits, pic)
#optimize_forest(digits, pic)
# show_output()



