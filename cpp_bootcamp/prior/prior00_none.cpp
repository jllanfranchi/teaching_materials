#include <iostream>
#include <sstream>
using namespace std;

class prior
{
	public:
		// constructor
		prior() : type("none"), str_info("") {}

		// pretty-print info
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }

		// log-likelihood
		double llh(double x) { return 0; }

		// chi-square, in terms of llh
		double chi2(double x) { return -2*llh(x); }

	private:
		// keep these things protected from evil callers!
		string type;
		string str_info;
};


int main(void)
{
	prior p;
	p.info();
	cout << "p.llh(1) = " << p.llh(1) << endl;
	cout << "p.chi2(1) = " << p.chi2(1) << endl << endl;

	cout << "p.llh(1) = " << p.llh(2) << endl;
	cout << "p.chi2(1) = " << p.chi2(2) << endl << endl;

	return 0;
};
