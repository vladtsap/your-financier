from models.core import ExtendedEnum
from utils import texts


class Categories(ExtendedEnum):
    AUTO = ('auto', texts.AUTO_CATEGORY)
    BOOKS = ('books', texts.BOOKS_CATEGORY)
    CLOTHES = ('clothes', texts.CLOTHES_CATEGORY)
    ENTERTAINMENT = ('entertainment', texts.ENTERTAINMENT_CATEGORY)
    FEES = ('fees', texts.FEES_CATEGORY)
    FOOD = ('food', texts.FOOD_CATEGORY)
    GIFTS = ('gifts', texts.GIFTS_CATEGORY)
    HEALTH = ('health', texts.HEALTH_CATEGORY)
    HOME = ('home', texts.HOME_CATEGORY)
    PAYMENT = ('payment', texts.PAYMENT_CATEGORY)
    SUPERMARKET = ('supermarket', texts.SUPERMARKET_CATEGORY)
    TRANSPORT = ('transport', texts.TRANSPORT_CATEGORY)
    TRAVEL = ('travel', texts.TRAVEL_CATEGORY)
    OTHER = ('other', texts.OTHER_CATEGORY)

    @classmethod
    def match(cls, mcc: int):

        if mcc in range(3351, 3442) or [
            5013, 5172, 5511, 5521, 5531, 5532, 5533, 5541, 5542, 5552, 5561, 5571, 5592, 5598, 5599,
            5935, 5983, 7511, 7512, 7513, 7519, 7523, 7524, 7531, 7534, 7535, 7538, 7542, 7549, 8675,
        ]:
            return cls.AUTO

        elif mcc in [5192, 5942, 5994]:
            return cls.BOOKS

        elif mcc in [
            5094, 5131, 5137, 5139, 5611, 5621, 5631, 5641, 5651, 5655, 5661, 5681, 5691, 5697, 5698,
            5699, 5931, 5948, 5949, 7251, 7296,
        ]:
            return cls.CLOTHES

        elif mcc in [
            5816, 7221, 7272, 7273, 7278, 7394, 7800, 7801, 7802, 7829, 7832, 7833, 7841, 7911, 7922,
            7929, 7932, 7933, 7941, 7993, 7994, 7995, 7996, 7997, 7998, 7999, 9406, 9754,
        ]:
            return cls.ENTERTAINMENT

        elif mcc in [
            6010, 6011, 6012, 6022, 6023, 6025, 6026, 6028, 6760, 7276, 7322, 9211, 9222, 9223, 9311,
            9399, 9405, 9411,
        ]:
            return cls.FEES

        elif mcc in [5811, 5812, 5813, 5814]:
            return cls.FOOD

        elif mcc in [5944, 5945, 5946, 5947, 5992]:
            return cls.GIFTS

        elif mcc in [
            4119, 5047, 5072, 5122, 5912, 5940, 5941, 5975, 5976, 5977, 5997, 7230, 7280, 7297, 7298,
            8011, 8021, 8031, 8041, 8042, 8043, 8044, 8049, 8062, 8071, 8099, 9702,
        ]:
            return cls.HEALTH

        elif mcc in [
            780, 1520, 1711, 1731, 1740, 1750, 1761, 1771, 2842, 4900, 5021, 5039, 5051, 5074, 5193,
            5198, 5200, 5211, 5231, 5251, 5261, 5271, 5299, 5712, 5713, 5714, 5718, 5719, 5722, 5732,
            5950, 6513, 7210, 7211, 7216, 7217, 7622, 7623, 7629, 7631, 7641, 7692, 7699, 8911,
        ]:
            return cls.HOME

        elif mcc in [
            3882, 4829, 6050, 6051, 6211, 6236, 6529, 6530, 6531, 6532, 6533, 6534, 6535, 6536, 6537,
            6538, 6539, 6540, 6611,
        ]:
            return cls.PAYMENT

        elif mcc in [
            743, 744, 5262, 5297, 5298, 5300, 5309, 5310, 5311, 5331, 5399, 5411, 5422, 5441, 5451,
            5462, 5499, 5715, 5921, 5993,
        ]:
            return cls.SUPERMARKET

        elif mcc in [4111, 4121, 4131, 4784, 5962]:
            return cls.TRANSPORT

        elif mcc in range(3000, 3303) or range(3501, 3839) or [
            4011, 4112, 4411, 4457, 4468, 4511, 4582, 4722, 4723, 4789, 5551, 7011, 7033, 7991, 7992,
        ]:
            return cls.TRAVEL

        else:
            return cls.OTHER
