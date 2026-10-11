public class Demo {
    interface Payment {
        String pay(int a,String r);
    }
    static class Card implements Payment {
        public String pay(int a,String r) {
            return "card";
        }
    }
    static class Wallet implements Payment {
        public String pay(int a,String r) {
            return "wallet";
        }
    }
    static class Billing {
        Payment p;
        Billing(Payment p) {
            this.p=p;
        }
        String checkout(int a,String r) {
            if(a<=0||r.isEmpty())throw new IllegalArgumentException();
            return p.pay(a,r);
        }
    }
    public static void main(String[]a) {
        if(!new Billing(new Card()).checkout(100,"B1").equals("card")||!new Billing(new Wallet()).checkout(100,"B1").equals("wallet"))throw new AssertionError();
    }
}
