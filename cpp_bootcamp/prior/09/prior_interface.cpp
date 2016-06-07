#include <iostream>
#include <sstream>
using namespace std;

/*
 * Pesky issues arise because our original assumptions about how `info()`
 * would work are violated with setters.
 *
 * Basically, what looked like it would be a generic function when we started
 * isn't. That's okay, it had its time; now make it a pure virtual function,
 * which each subclass must implement on its own.
 *
 *  (NOTE: We could divide 'info' up such that 'name' is still generic but
 *  'str_info' is the pure virtual function that children must implement.)
 *
 * This just leaves the `chi2` method as the sole function implemented in the
 * `prior` class.
 *
 * Also: introduce the 'override' keyword.
 *
 */


class prior
{
	public:
		virtual void info() = 0;
		double chi2(double x) { return -2*llh(x); }
		virtual double llh(double) = 0;
};


class none
	: public prior
{
	public:
		none() {}

		// 'override' keyword added so compiler knows our
		// intentions, checks
		// that no typo's
		virtual double llh(double x) override { return 0; }

		// Must implement this method here now
		virtual void info() override { cout << "prior : none" << endl; }
};


class uniform
	: public virtual prior
{
	public:
		uniform(double offset)
			: offset(offset) {}
								// 'prior' default constructor is fine
		virtual double llh(double x) override { return offset; }
		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

		//
		virtual void info() override {
			cout << "prior : uniform, offset = " << offset << endl;
		}

	private:
		double offset;
};


class gaussian
	: public virtual prior
{
	public:
		gaussian(double mean, double stddev) : mean(mean), stddev(stddev) {}
		double llh(double x) override {
			return -(x-mean)*(x-mean)/(2*stddev*stddev);
		}

		//
		virtual void info() override {
			cout << "prior : Gaussian, mean = " << mean << ", stddev = "
				<< stddev << endl;
		}

		double get_mean() { return mean; }
		double get_stddev() { return stddev; }

	private:
		const double mean;
		const double stddev;
};


class offset_gaussian
	: public gaussian, public uniform
{
	public:
		offset_gaussian(double offset, double mu, double sigma)
			: prior(), gaussian(mu, sigma), uniform(offset) {}

		virtual double llh(double x) override { return uniform::llh(x) + gaussian::llh(x); }

		virtual void info() override {
			cout << "prior : offset Gaussian, offset = " << get_offset()
				<< ", mean = " << get_mean() << ", stddev = " << get_stddev() << endl;
		}
};


double llh_freefunc(prior& p, double x) {
	return p.llh(x);
}


double chi2_freefunc(prior *p, double x) {
	return p->chi2(x);
}


// Add function for printing to reduce copy-paste
void report(prior& p, const string &name) {
	cout << "  " << name << ".info() :\n    "; p.info();
	cout << "  llh_freefunc(" << name << ", 1)  = " << llh_freefunc(p, 1) << endl;
	cout << "  " << name << ".chi2(1)           = " << p.chi2(1) << endl << endl;
}


int main(void)
{
	// Create a 'none' prior, and print info about it
	cout << "none n;" << endl;
	none n;
	report(n, "n");

	// Create a 'uniform' prior, and print info about it
	cout << "uniform u(-0.2);" << endl;
	uniform u(-0.2);
	report(u, "u");

	// Create a 'gaussian' prior, and print info about it
	cout << "gaussian g(0, 1);" << endl;
	gaussian g(0, 1);
	report(g, "g");

	// Create an 'offset_gaussian' prior, and print info about it
	cout << "offset_gaussian(-10, 0, 1);" << endl;
	offset_gaussian og(-10, 0, 1);
	report(og, "og");

	cout << endl;

	cout << "og.get_offset() = " << og.get_offset() << endl;
	cout << "og.set_offset(-1);" << endl;
	og.set_offset(-1);
	cout << "og.get_offset() = " << og.get_offset() << endl;

	cout << endl;

	report(og, "og");

	return 0;
};
