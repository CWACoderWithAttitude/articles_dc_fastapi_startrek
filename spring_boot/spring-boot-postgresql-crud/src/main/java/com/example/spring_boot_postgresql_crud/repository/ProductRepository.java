package com.example.spring_boot_postgresql_crud.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.spring_boot_postgresql_crud.model.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {
}
