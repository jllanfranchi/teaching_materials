#include <iostream>
#include <sstream>
using namespace std;


class prior
{
	public:
		prior(const string &type, const string &str_info)
			: type(type), str_info(str_info) {}
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		double chi2(double x) { return -2*llh(x); }
		virtual double llh(double) = 0;

	private:
		const string type;
		const string str_info;
};


class none
	: public prior
{
	public:
		none() : prior("none", "") {}
		virtual double llh(double x) { return 0; }
};

class uniform
	: public prior
{
	public:
		uniform(double offset)
			: offset(offset),
			prior("uniform", "offset = " + to_string(offset)) {}
		virtual double llh(double x) { return offset; }
		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

	private:
		double offset;
};


class gaussian
	: public prior
{
	public:
		gaussian(double mean, double stddev) : mean(mean), stddev(stddev),
			prior("Gaussian", "mean = " + to_string(mean) + ", stddev = "
					+ to_string(stddev)) {}
		double llh(double x) { return -(x-mean)*(x-mean)/(2*stddev*stddev); }
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }

	private:
		const double mean;
		const double stddev;
};

// Offset Gaussian derives from 'gaussian' and 'uniform'
class offset_gaussian
	: public gaussian, public uniform
{
	public:
		// NOTE: can't initialize 'prior' base since it isn't a parent
		offset_gaussian(double ofst, double mu, double sigma)
			: uniform(ofst), gaussian(mu, sigma) {}
		virtual double llh(double x) { return uniform::llh(x) + gaussian::llh(x); }
};


double llh_freefunc(prior& p, double x) {
	return p.llh(x);
}

double chi2_freefunc(prior *p, double x) {
	return p->chi2(x);
}


int main(void)
{
	// Create a 'none' prior, and print info about it
	none n;
	n.info();
	cout << "llh_freefunc(n, 1) = " << llh_freefunc(n, 1) << endl;
	cout << "chi2_freefunc(&n, 1) = " << chi2_freefunc(&n, 1) << endl;
	cout << "llh_freefunc(n, 2) = " << llh_freefunc(n, 2) << endl;
	cout << "chi2_freefunc(&n, 2) = " << chi2_freefunc(&n, 2) << endl;

	cout << endl;

	// Create a 'uniform' prior, and print info about it
	uniform u(-0.2);
	u.info();
	cout << "llh_freefunc(u, 1) = " << llh_freefunc(u, 1) << endl;
	cout << "chi2_freefunc(&u, 1) = " << chi2_freefunc(&u, 1) << endl;
	cout << "llh_freefunc(u, 2) = " << llh_freefunc(u, 2) << endl;
	cout << "chi2_freefunc(&u, 2) = " << chi2_freefunc(&u, 2) << endl;

	cout << endl;

	// Create a 'gaussian' prior, and print info about it
	gaussian g(0, 1);
	g.info();
	cout << "llh_freefunc(g, 1) = " << llh_freefunc(g, 1) << endl;
	cout << "chi2_freefunc(&g, 1) = " << chi2_freefunc(&g, 1) << endl;
	cout << "llh_freefunc(g, 2) = " << llh_freefunc(g, 2) << endl;
	cout << "chi2_freefunc(&g, 2) = " << chi2_freefunc(&g, 2) << endl;

	cout << endl;

	// Create an 'offset_gaussian' prior, and print info about it
	cout << "offset_gaussian og(-10, 0, 1);" << endl;
	offset_gaussian og(-10, 0, 1);
	og.info();
	cout << "llh_freefunc(og, 1) = " << llh_freefunc(og, 1) << endl;
	cout << "chi2_freefunc(&og, 1) = " << chi2_freefunc(&og, 1) << endl;
	cout << "llh_freefunc(og, 2) = " << llh_freefunc(og, 2) << endl;
	cout << "chi2_freefunc(&og, 2) = " << chi2_freefunc(&og, 2) << endl;

	cout << endl;

	cout << "og.get_offset() = " << og.get_offset() << endl;
	cout << "og.set_offset(-1);" << endl;
	og.set_offset(-1);
	cout << "og.get_offset() = " << og.get_offset() << endl;
	cout << "og.info();" << endl;
	og.info();
	cout << "og.llh(1) = " << og.llh(1) << endl;
	cout << "og.chi2(1) = " << og.chi2(1) << endl << endl;

	return 0;
};
