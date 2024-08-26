from enum import Enum, auto


class Level(Enum):
    is_low = auto()
    is_normal = auto()
    is_high = auto()


class KcalLevel:
    """
    calculate the total amount of calories from macronutrients and determine
    the calorie level based on pre-defined ranges.
    """

    @staticmethod
    def calculate_kcal(cho, ptn, fat):
        return (cho * 4) + (ptn * 4) + (fat * 9)

    @staticmethod
    def calculate_kcal_level(kcal):
        if kcal < 1500:
            return Level.is_low.name
        elif kcal <= 2000:
            return Level.is_normal.name
        else:
            return Level.is_high.name


class CalcMacroLevel:
    """
    Calculates and classifies the macronutrient based on the total energy value (i.e. total calories/day).
    """

    @staticmethod
    def calculate_level(amount, kcal, kcal_per_unit, low_threshold, high_threshold):
        """
        calculate the level of any macronutrient. It considers the amount of macronutrient (in grams),
        the total calories in the diet, the calories provided per unit of the macronutrient and the classification
        thresholds (low, normal, high).
        """
        # Calculates the energy value of the macronutrient
        nutrient_kcal = amount * kcal_per_unit
        # Calculates the percentage of the nutrient in relation to the total caloric value
        percentage = nutrient_kcal / kcal * 100

        # Determines level based on percentage
        if percentage < low_threshold:
            return Level.is_low.name
        elif percentage <= high_threshold:
            return Level.is_normal.name
        else:
            return Level.is_high.name

    def calculate_macro_level(self, amount, kcal, macro_type):
        thresholds = {
            'cho': (4, 55, 75),
            'fat': (9, 15, 30),
            'ptn': (4, 10, 15),
        }

        if macro_type not in thresholds:
            raise ValueError(f"Invalid macro_type: {macro_type}")

        kcal_per_unit, low_threshold, high_threshold = thresholds[macro_type]
        return self.calculate_level(amount, kcal, kcal_per_unit, low_threshold, high_threshold)


class ProportionGKG:
    """
    Calculates the gram/kg ratio, divides the macronutrient value by the individual's weight
    """

    def __init__(self, weight, cho, ptn, fat):
        self.cho_proportion = cho / weight
        self.ptn_proportion = ptn / weight
        self.fat_proportion = fat / weight


if __name__ == "__main__":
    cho = 250  # gramas
    ptn = 100  # gramas
    fat = 80  # gramas
    weight = 70  # kg

    # 1. Calcular o total de calorias usando KcalLevel
    total_kcal = KcalLevel.calculate_kcal(cho, ptn, fat)
    print(f"Total de calorias: {total_kcal}")

    # 2. Determinar o nível de calorias usando KcalLevel
    kcal_level = KcalLevel.calculate_kcal_level(total_kcal)
    print(f"Nível de calorias: {kcal_level}")

    # 3. Calcular os níveis de macronutrientes usando CalcMacroLevel
    calc_macro = CalcMacroLevel()

    cho_level = calc_macro.calculate_macro_level(cho, total_kcal, 'cho')
    ptn_level = calc_macro.calculate_macro_level(ptn, total_kcal, 'ptn')
    fat_level = calc_macro.calculate_macro_level(fat, total_kcal, 'fat')

    print(f"Nível de carboidratos (CHO): {cho_level}")
    print(f"Nível de proteínas (PTN): {ptn_level}")
    print(f"Nível de gorduras (FAT): {fat_level}")

    # 4. Calcular as proporções gramas por kg usando ProportionGKG
    proportions = ProportionGKG(weight, cho, ptn, fat)

    print(f"Proporção de carboidratos (CHO) por kg: {proportions.cho_proportion:.2f}")
    print(f"Proporção de proteínas (PTN) por kg: {proportions.ptn_proportion:.2f}")
    print(f"Proporção de gorduras (FAT) por kg: {proportions.fat_proportion:.2f}")
