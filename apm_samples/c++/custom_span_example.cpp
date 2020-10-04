#include <datadog/opentracing.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <unistd.h>

using namespace std;
class ClassA {

public:
	void add_balance(int val);
        int get_balance(void);

private:
	int balance;
};

int ClassA::get_balance(void) {
	
	return balance;
}
void ClassA::add_balance(int val) {
	balance += val;
        cout << "current_balance: " << balance << " after add_balance(" << val <<")\n";
}

int main(int argc, char* argv[]) {

        datadog::opentracing::TracerOptions tracer_options{"localhost", 8126, "compiled-in example"};
        auto tracer = datadog::opentracing::makeTracer(tracer_options);


        for(;;) {
        	ClassA a;
        
                auto span_a = tracer->StartSpan("A");
        
                auto span_b = tracer->StartSpan("B", {opentracing::ChildOf(&span_a->context())});
                int value = rand() % 10000 + 1;
                a.add_balance(value);
                span_b->SetTag("adding_value", value);
                span_b->Finish();
        
                auto span_c = tracer->StartSpan("C", {opentracing::ChildOf(&span_a->context())});
                auto current_balance = a.get_balance();
                span_c->SetTag("current_balance", current_balance);
                span_c->Finish();
        
                span_a->Finish(); 
                if( current_balance > 1000000 ) {
                        cout << "Exiting the loop current balance is "<< current_balance << "\n";
                        break;
                }
                usleep(100000);
        }       
        tracer->Close();
	return 0;
}
