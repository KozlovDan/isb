import java.util.Random;

public class RandomGenerator {
    
    /**
     * Генерирует и выводит случайную битовую последовательность длиной 128 бит
     * Используется Random для создания последовательности.
     * 
     * @param args Аргументы командной строки
     */
    public static void main(String[] args) {
        SecureRandom random = new SecureRandom();
        StringBuilder binaryString = new StringBuilder();
        
        for (int i = 0; i < 128; i++) {
            binaryString.append(random.nextBoolean() ? '1' : '0');
        }
        
        System.out.println("Сгенерированная последовательность (128 бит):");
        System.out.println(binaryString.toString());
    }
}