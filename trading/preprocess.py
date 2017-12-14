import quandl
from trading import constants


class Gather(object):

    def __init__(self, company, api_key, sd, ed, index=4):
        """Initialise the constructor for
        data collection module that fetches the stock
        data from Quandl with the specified index number
        and the timestamp

        :param company: Company to fetch the stock of
        :param api_key: Quandl API key
        :param sd: starting date
        :param ed: ending date
        :param index: Column to fetch
        """
        company_token = constants.COMPANIES[company]
        self._data = quandl.get(company_token,
                                authtoken=api_key,
                                start_date=sd,
                                end_date=ed,
                                column_index=index)

    @property
    def data(self):
        return self._data.reset_index()

    def write_csv(self, path):
        self.data.to_csv(path, index=False)
