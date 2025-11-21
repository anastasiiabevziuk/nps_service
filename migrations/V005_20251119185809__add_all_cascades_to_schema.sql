
ALTER TABLE PHOTOSESSION
    DROP CONSTRAINT photosession_model_id_fkey;


ALTER TABLE PHOTOSESSION
    ADD CONSTRAINT photosession_model_id_fkey
    FOREIGN KEY (model_id)
    REFERENCES MODEL (model_id)
    ON DELETE CASCADE;


ALTER TABLE PHOTOSESSION
    DROP CONSTRAINT photosession_photographer_id_fkey; 


ALTER TABLE PHOTOSESSION
    ADD CONSTRAINT photosession_photographer_id_fkey
    FOREIGN KEY (photographer_id)
    REFERENCES PHOTOGRAPHER (photographer_id)
    ON DELETE CASCADE;


ALTER TABLE PHOTO
    DROP CONSTRAINT photo_photosession_id_fkey;


ALTER TABLE PHOTO
    ADD CONSTRAINT photo_photosession_id_fkey
    FOREIGN KEY (photosession_id)
    REFERENCES PHOTOSESSION (photosession_id)
    ON DELETE CASCADE;