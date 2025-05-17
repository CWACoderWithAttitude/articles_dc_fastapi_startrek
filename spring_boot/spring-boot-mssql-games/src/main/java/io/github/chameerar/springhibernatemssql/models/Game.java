package io.github.chameerar.springhibernatemssql.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Entity
@Getter
@Setter
@ToString
public class Game {

    @Id
    @GeneratedValue
    private Long id;
    private String title;

    public Game() {
    }

    public Game(String title) {
        this.title = title;
    }

    public Long getId() {

        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }
}
