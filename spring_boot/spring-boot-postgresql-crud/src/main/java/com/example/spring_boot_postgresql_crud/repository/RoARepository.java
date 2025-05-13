package com.example.spring_boot_postgresql_crud.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.spring_boot_postgresql_crud.model.RoA;

public interface RoARepository extends JpaRepository<RoA, Long> {
}
