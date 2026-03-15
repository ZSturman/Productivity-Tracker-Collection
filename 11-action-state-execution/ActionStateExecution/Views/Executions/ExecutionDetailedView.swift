//
//  ActionStateDetailedView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//
import SwiftUI
import MapKit

struct ExecutionDetailedView: View {
    let execution: ExecutionEntity
    
    @Environment(\.managedObjectContext) var moc
    @Environment(\.dismiss) var dismiss
    @State private var showingDeleteAlert = false

    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 34.011_286, longitude: -116.166_868),
        span: MKCoordinateSpan(latitudeDelta: 0.2, longitudeDelta: 0.2)
    )
    
    var fieldValues: [FieldValueEntity] {
        return execution.fieldValues?.allObjects as? [FieldValueEntity] ?? []
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            executionDetailHeader
            fieldValuesList
            coordinatesView
            mapAndLocationInfo
        }
        .padding()
        .navigationTitle("\(execution.timestamp ?? Date())")
        .toolbar {
            deleteButton
        }
    }
    
    private var executionDetailHeader: some View {
        VStack(alignment: .leading) {
            Text("Details for \(execution.actionStateID?.name ?? "")")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Timestamp: \(execution.timestamp ?? Date())")
                .font(.body)
                .foregroundColor(.secondary)
        }
    }
    
    private var fieldValuesList: some View {
        List {
            ForEach(fieldValues, id: \.id) { fieldValue in
                VStack(alignment: .leading) {
                    Text("Field Name: \(fieldValue.fieldID?.fieldName ?? "")")
                    Text("Value: \(fieldValue.value ?? "")")
                }
            }
        }
    }
    
    private var coordinatesView: some View {
        VStack(alignment: .leading) {
            Text("Coordinates:")
                .font(.headline)
            
            Text("\(execution.latitude), \(execution.longitude)")
                .font(.body)
                .foregroundColor(.secondary)
        }
    }
    
    private var mapAndLocationInfo: some View {
        VStack(alignment: .leading) {
            Map(coordinateRegion: $region)
                .onAppear {
                    setRegion(execution.latitude, execution.longitude)
                }
            
            Text(execution.actionStateID?.collectDate ?? false ? "Collects Date" : "Does not collect Date")
                .font(.caption)
                .foregroundColor(execution.actionStateID?.collectDate ?? false ? .green : .red)
            
            Text(execution.actionStateID?.collectTime ?? false ? "Collects Time" : "Does not collect Time")
                .font(.caption)
                .foregroundColor(execution.actionStateID?.collectTime ?? false ? .green : .red)
                
            Text(execution.actionStateID?.collectLocation ?? false ? "Collects Location" : "Does not collect Location")
                .font(.caption)
                .foregroundColor(execution.actionStateID?.collectLocation ?? false ? .green : .red)
        }
    }
    
    private var deleteButton: some View {
        Button {
            showingDeleteAlert = true
        } label : {
            Label("Delete Execution", systemImage: "trash")
        }
        .alert("Delete Execution?", isPresented: $showingDeleteAlert) {
            Button("Delete", role: .destructive, action: deleteExecution)
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Are you sure?")
        }
    }
    
    func deleteExecution() {
        moc.delete(execution)
        dismiss()
    }
    
    private func setRegion(_ latitude: Double?, _ longitude: Double?) {
        let lat = latitude ?? 0.0
        let long = longitude ?? 0.0
        region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: lat, longitude: long),
            span: MKCoordinateSpan(latitudeDelta: 0.2, longitudeDelta: 0.2)
        )
    }
}
