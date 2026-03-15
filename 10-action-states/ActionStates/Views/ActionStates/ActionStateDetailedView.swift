//
//  ActionStateDetailedView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//

import SwiftUI
import MapKit


struct ActionStateDetailedView: View {
    let actionState: ActionStateEntity
    
    @Environment(\.managedObjectContext) var moc
    @Environment(\.dismiss) var dismiss
    @State private var showingDeleteAlert = false


    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 34.011_286, longitude: -116.166_868),
        span: MKCoordinateSpan(latitudeDelta: 0.2, longitudeDelta: 0.2)
    )

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Details for \(actionState.name ?? "")")
                .font(.title)
                .fontWeight(.bold)
                
            Text("Explanation:")
                .font(.headline)
            Text(actionState.explanation ?? "")
                .font(.body)
                .foregroundColor(.secondary)
            
            List {
                ForEach(actionState.manualInputs?.allObjects as? [ManualInputEntity] ?? [], id: \.id) { manualInput in
                    Text(manualInput.inputType ?? "")
                }
            }

            Text("Coordinates:")
                .font(.headline)
            Text("\(actionState.latitude), \(actionState.longitude)")
                .font(.body)
                .foregroundColor(.secondary)
            
            Map(coordinateRegion: $region)
                .onAppear {
                    setRegion(actionState.latitude, actionState.longitude)
                }
            
            Text(actionState.collectDate ? "Collects Date" : "Does not collect Date")
                .font(.caption)
                .foregroundColor(actionState.collectDate ? .green : .red)
            
            Text(actionState.collectTime ? "Collects Time" : "Does not collect Time")
                .font(.caption)
                .foregroundColor(actionState.collectTime ? .green : .red)
                
            Text(actionState.collectLocation ? "Collects Location" : "Does not collect Location")
                .font(.caption)
                .foregroundColor(actionState.collectLocation ? .green : .red)
            
        }
        .padding()
        .navigationTitle(actionState.name ?? "")
        .alert("Delete ActionState?", isPresented: $showingDeleteAlert) {
            Button("Delete", role: .destructive, action: deleteActionState)
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Are you sure?")
        }
        .toolbar {
            Button {
                showingDeleteAlert = true
            } label : {
                Label("Delete ActionState", systemImage: "trash")
            }
        }
    }
    
    func deleteActionState() {
        moc.delete(actionState)
        
        //try? moc.save()
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
