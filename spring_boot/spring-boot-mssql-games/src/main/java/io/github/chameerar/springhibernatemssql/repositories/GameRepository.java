package io.github.chameerar.springhibernatemssql.repositories;

import io.github.chameerar.springhibernatemssql.models.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import io.github.chameerar.springhibernatemssql.models.Game;

@Repository
public interface GameRepository extends JpaRepository<Game, Long> {

}
