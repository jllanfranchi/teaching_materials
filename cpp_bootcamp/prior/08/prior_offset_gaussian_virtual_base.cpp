#include <iostream>
#include <sstream>
using namespace std;

class prior
{
	public:
		prior(const string &type, const string &str_info)
			: type(type), str_info(str_info) {}
		void info() {
			cout << "prior : " << type << " ; " << str_info << endl;
		}
		double chi2(double x) { return -2*llh(x); }
		virtual double llh(double) = 0;

	protected:
		string type;
		string str_info;
};

class none
	: public prior
{
	public:
		none() : prior("none", "") {}
		virtual double llh(double x) { return 0; }
};

class uniform
	// Make prior a virtual base class
	: public virtual prior
{
	public:
		uniform(double offset) : offset(offset),
			prior("uniform", "offset = " + to_string(offset)) {}
		virtual double llh(double x) { return offset; }
		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

	protected:
		double offset;
};

class gaussian
	// Make prior a virtual base class
	: public virtual prior
{
	public:
		gaussian(double mean, double stddev) : mean(mean), stddev(stddev),
			prior("Gaussian", "mean = " + to_string(mean) + ", stddev = "
					+ to_string(stddev)) {}
		double llh(double x) { return -(x-mean)*(x-mean)/(2*stddev*stddev); }
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }

	protected:
		double mean;
		double stddev;
};

class offset_gaussian
	: public gaussian, public uniform
{
	public:
		offset_gaussian(double ofst, double mu, double sigma)
			: prior("offset Gaussian", "offset = " + to_string(ofst)
					+ ", mean = " + to_string(mu)
					+ ", stddev = " + to_string(sigma)),
			gaussian(mu, sigma), uniform(ofst) {}

		virtual double llh(double x) { return uniform::llh(x) + gaussian::llh(x); }
		double get_offset() { return offset; }
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }
		void set_offset(double ofst) { offset = ofst; }
		void set_mean(double mu) { mean = mu; }
		void set_stddev(double sigma) { stddev = sigma; }
};


double llh_freefunc(prior& p, double x) {
	return p.llh(x);
}


int main(void)
{
	none n;
	cout << "llh_freefunc(n, 1) = " << llh_freefunc(n, 1) << endl;

	uniform u(-0.2);
	cout << "llh_freefunc(u, 1) = " << llh_freefunc(u, 1) << endl;

	gaussian g(0, 1);
	cout << "llh_freefunc(g, 1) = " << llh_freefunc(g, 1) << endl << endl;

	offset_gaussian og(-10, 0, 1);
	cout << "og.info() = ";
	og.info();
	cout << "llh_freefunc(og, 1) = " << llh_freefunc(og, 1) << endl;
	cout << "og.chi2(1) = " << og.chi2(1) << endl << endl;

	cout << endl;
	cout << "og.set_offset(-1); og.set_stddev(3);" << endl;
	og.set_offset(-1);
	og.set_stddev(3);
	cout << "og.get_offset();" << og.get_offset() << endl;
	cout << "og.get_stddev();" << og.get_stddev() << endl;
	cout << "og.info();" << endl;
	og.info();
	cout << "og.chi2(1) = " << og.chi2(1) << endl << endl;

	return 0;
};
