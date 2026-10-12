from pydantic import BaseModel


class Utill(BaseModel):
    
    tempo: float

    def convCelcius(self) -> float:
        return (self.tempo * (9 / 5)) + 32
    
    def convFahrenheit(self) -> float:
            return ((self.tempo -32 ) * (5 / 9)) + 273.15
    

# formulas
# fahrenheit para kelvin
# k = (f -32)x(5/9) + 273.15

# kelvin para fahrenheit
# F=(K-273.15)x(9/5)+32

# celsius para fahrenheit
# f = ( c x (9/5))+32

# c = (f-32)x(5/9)
