package com.example.spring_boot_postgresql_crud.service;

import java.util.List;
import java.util.Optional;

import com.example.spring_boot_postgresql_crud.model.ProductDTO;

public interface ProductService {
    List<ProductDTO> getAllProducts();

    Optional<ProductDTO> getProductById(Long id);

    ProductDTO saveProduct(ProductDTO productDTO);

    ProductDTO updateProduct(Long id, ProductDTO productDTO);

    void deleteProduct(Long id);
}
