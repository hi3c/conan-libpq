#include <iostream>
#include <libpq-fe.h>

int main() {
  PGconn *conn;
  conn = PQconnectdb("dbname=postgres");
  if (PQstatus(conn) != CONNECTION_OK)
  {
    std::cout << "Connection failed (which is ok): " << PQerrorMessage(conn) << std::endl;
  }

  return 0;
}
